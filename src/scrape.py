"""Walk the user's leagues, scrape every completed round, write a parquet table.

Schema (one row per song):
    league, league_id, round, round_id, player, submitter_user_id,
    song, artist, spotify_track_id, score,
    votes: list[struct{voter: str | null, votes: int}]
"""

from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from pathlib import Path

import polars as pl

from src.auth import parse_curl_file
from src.client import MusicLeagueClient
from src.log import install as install_logger
from src.names import anonymise_dataframe
from src.parse import (
    LeagueTile,
    RoundEntry,
    SongRow,
    parse_landing,
    parse_league,
    parse_round,
)

logger = logging.getLogger(__name__)

_DEFAULT_AUTH = Path("auth.curl")
_DEFAULT_OUT = Path("out/music_league.parquet")
_DEFAULT_CSV = Path("out/music_league.csv")
_DEFAULT_LOG = Path("logs/scrape.log")
_CSV_COLUMNS = ("round_time", "league", "round", "player", "song", "artist", "score")
_SORT_BY = ("round_time", "player")


@dataclass(frozen=True)
class Args:
    auth: Path
    out: Path
    csv: Path
    log: Path
    sleep: float
    league_filter: list[str] | None
    debug: bool
    debug_dir: Path


def main() -> None:
    args = _parse_args()
    install_logger(args.log, debug=args.debug)
    logger.info(
        "starting scrape: out=%s csv=%s sleep=%.2f debug=%s",
        args.out,
        args.csv,
        args.sleep,
        args.debug,
    )

    auth = parse_curl_file(args.auth)
    with MusicLeagueClient(auth, sleep_seconds=args.sleep) as client:
        client_get = client.get_html
        if args.debug:
            args.debug_dir.mkdir(parents=True, exist_ok=True)
            client.get_html = _wrap_dump(client_get, args.debug_dir)  # type: ignore[method-assign]
        rows = list(_scrape_all(client, league_filter=args.league_filter))

    df = anonymise_dataframe(_to_dataframe(rows)).sort(list(_SORT_BY))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(args.out)
    logger.info("wrote %d rows to %s", df.height, args.out)

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    df.select(_CSV_COLUMNS).write_csv(args.csv)
    logger.info("wrote %d rows to %s", df.height, args.csv)

    _print_league_summary(df)
    print("\nExample rows (random sample of 5):")
    print(df.sample(n=min(5, df.height)) if df.height else df)


def _print_league_summary(df: pl.DataFrame) -> None:
    if df.height == 0:
        print("\nNo completed leagues found.")
        return
    summary = (
        df.group_by("league")
        .agg(
            pl.col("round_id").n_unique().alias("rounds"),
            pl.len().alias("songs"),
        )
        .sort("league")
    )
    print("\nLeagues with completed rounds:")
    for row in summary.iter_rows(named=True):
        print(f"  {row['league']}: {row['rounds']} rounds, {row['songs']} songs")


def _parse_args() -> Args:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--auth", type=Path, default=_DEFAULT_AUTH)
    p.add_argument("--out", type=Path, default=_DEFAULT_OUT)
    p.add_argument("--csv", type=Path, default=_DEFAULT_CSV)
    p.add_argument("--log", type=Path, default=_DEFAULT_LOG)
    p.add_argument("--sleep", type=float, default=0.5, help="seconds between requests")
    p.add_argument(
        "--league",
        action="append",
        dest="leagues",
        help="limit to one or more league IDs (repeat the flag); default = all",
    )
    p.add_argument(
        "--debug",
        action="store_true",
        help="DEBUG-level logs and dump every fetched HTML to --debug-dir",
    )
    p.add_argument("--debug-dir", type=Path, default=Path("debug"))
    ns = p.parse_args()
    return Args(
        auth=ns.auth,
        out=ns.out,
        csv=ns.csv,
        log=ns.log,
        sleep=ns.sleep,
        league_filter=ns.leagues,
        debug=ns.debug,
        debug_dir=ns.debug_dir,
    )


def _wrap_dump(get_html, debug_dir: Path):
    """Wrap a ``client.get_html`` call to also persist the response to disk."""

    def wrapped(path: str) -> str:
        html = get_html(path)
        safe = path.strip("/").replace("/", "__") or "root"
        target = debug_dir / f"{safe}.html"
        target.write_text(html)
        logger.debug("dumped %s (%d bytes) -> %s", path, len(html), target)
        return html

    return wrapped


_LEAGUE_LIST_FRAGMENTS = (
    "/completed/-/completedLeagues",
    "/home/-/currentLeagues",
)


def _scrape_all(client: MusicLeagueClient, *, league_filter: list[str] | None) -> list[SongRow]:
    tiles = _discover_leagues(client)
    if league_filter:
        wanted = set(league_filter)
        tiles = [t for t in tiles if t.league_id in wanted]
    logger.info("found %d leagues to scrape", len(tiles))

    rows: list[SongRow] = []
    for tile in tiles:
        rows.extend(_scrape_league(client, tile))
    return rows


def _discover_leagues(client: MusicLeagueClient) -> list[LeagueTile]:
    """Fetch the htmx fragments that render league tiles and merge them.

    The home page (``/home/``) does not include tiles in its initial HTML — it
    fires htmx ``GET`` calls on load. We hit those endpoints directly:
    ``/completed/-/completedLeagues`` for finished leagues and
    ``/home/-/currentLeagues`` for in-progress ones.
    """
    seen: set[str] = set()
    tiles: list[LeagueTile] = []
    for path in _LEAGUE_LIST_FRAGMENTS:
        fragment = client.get_html(path)
        for tile in parse_landing(fragment):
            if tile.league_id in seen:
                continue
            seen.add(tile.league_id)
            tiles.append(tile)
        logger.debug("after %s: %d unique tiles", path, len(tiles))
    return tiles


def _scrape_league(client: MusicLeagueClient, tile: LeagueTile) -> list[SongRow]:
    logger.info("league %s (%s) status=%s", tile.name, tile.league_id, tile.status)
    rounds_html = client.get_html(f"/l/{tile.league_id}/-/rounds")
    league = parse_league(rounds_html)
    completed = [r for r in league.rounds if r.status == "COMPLETE"]
    logger.info("  %d/%d rounds complete", len(completed), len(league.rounds))

    rows: list[SongRow] = []
    for entry in completed:
        rows.extend(_scrape_round(client, tile, entry))
    return rows


def _scrape_round(client: MusicLeagueClient, tile: LeagueTile, entry: RoundEntry) -> list[SongRow]:
    html = client.get_html(f"/l/{tile.league_id}/{entry.round_id}/-/results")
    rnd = parse_round(
        html,
        league=tile.name,
        league_id=tile.league_id,
        round_id=entry.round_id,
        round_time=entry.time,
        round_name=entry.name,
    )
    logger.info("    round %s: %d songs", rnd.name, len(rnd.songs))
    return rnd.songs


_VOTES_DTYPE = pl.List(pl.Struct({"voter": pl.Utf8, "votes": pl.Int64}))


def _to_dataframe(rows: list[SongRow]) -> pl.DataFrame:
    if not rows:
        return pl.DataFrame(schema={**_SCHEMA, "votes": _VOTES_DTYPE})

    return pl.DataFrame(
        {
            "round_time": [r.round_time for r in rows],
            "league": [r.league for r in rows],
            "league_id": [r.league_id for r in rows],
            "round": [r.round for r in rows],
            "round_id": [r.round_id for r in rows],
            "player": [r.player for r in rows],
            "submitter_user_id": [r.submitter_user_id for r in rows],
            "song": [r.song for r in rows],
            "artist": [r.artist for r in rows],
            "spotify_track_id": [r.spotify_track_id for r in rows],
            "score": [r.score for r in rows],
            "votes": [[{"voter": v.voter, "votes": v.votes} for v in r.votes] for r in rows],
        },
        schema_overrides={"votes": _VOTES_DTYPE, "round_time": pl.Datetime("us", "UTC")},
    )


_SCHEMA: dict[str, pl.DataType] = {
    "round_time": pl.Datetime("us", "UTC"),
    "league": pl.Utf8,
    "league_id": pl.Utf8,
    "round": pl.Utf8,
    "round_id": pl.Utf8,
    "player": pl.Utf8,
    "submitter_user_id": pl.Utf8,
    "song": pl.Utf8,
    "artist": pl.Utf8,
    "spotify_track_id": pl.Utf8,
    "score": pl.Int64,
}


if __name__ == "__main__":
    main()
