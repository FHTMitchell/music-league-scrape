"""Read ``out/music_league.parquet`` and write a Markdown analysis report.

Run after ``python -m src.scrape`` has produced the parquet. Each section is
a self-contained polars query — adding a new analysis is just appending one
function and one section in :func:`main`.
"""

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

import markdown
import matplotlib.pyplot as plt
import numpy as np
import polars as pl
from matplotlib.colors import TwoSlopeNorm
from tabulate import tabulate

from src.log import install as install_logger

logger = logging.getLogger(__name__)

_DEFAULT_INPUT = Path("out/music_league.parquet")
_DEFAULT_OUTPUT_MD = Path("out/analysis.md")
_DEFAULT_OUTPUT_HTML = Path("out/analysis.html")
_DEFAULT_HEATMAP = Path("out/fan_hater_heatmap.png")
_DEFAULT_LOG = Path("logs/analyze.log")
_TOP_N = 10
_FAN_HATER_PLAYERS = 20  # cap the per-player table so the report stays readable
_LEFT_LEAGUE = "[Left the league]"  # placeholder Music League shows for departed users


@dataclass(frozen=True)
class Section:
    """One analysis block: ``## title``, optional intro ``header``, then a table.

    An ``image`` may be supplied alongside or instead of a table; the image is
    embedded as a markdown ``![title](path)`` link (relative path is fine when
    the markdown and image sit in the same directory).
    """

    title: str
    header: str | None
    table: pl.DataFrame | None = None
    rank: bool = True  # if True and table is set, prepend a 1-based 'rank' column
    image: Path | None = None

    def to_md(self) -> str:
        parts = [f"## {self.title}"]
        if self.header:
            parts.append(f"_{self.header}_")
        if self.image is not None:
            parts.append(f"![{self.title}]({self.image.name})")
        if self.table is not None:
            body = _with_rank(self.table) if self.rank else self.table
            parts.append(_md_table(body))
        return "\n\n".join(parts)


@dataclass(frozen=True)
class Args:
    parquet: Path
    md_out: Path
    html_out: Path
    heatmap_out: Path
    log: Path


def main() -> None:
    args = _parse_args()
    install_logger(args.log)

    if not args.parquet.exists():
        sys.exit(
            f"{args.parquet} not found. Run the scraper first:\n    uv run python -m src.scrape\n"
        )

    df = _load(args.parquet)
    args.heatmap_out.parent.mkdir(parents=True, exist_ok=True)
    _render_fan_hater_heatmap(df, args.heatmap_out)
    logger.info("wrote heatmap to %s", args.heatmap_out)
    sections = _build_sections(df, heatmap=args.heatmap_out)
    md_text = _compile_markdown(sections)

    args.md_out.parent.mkdir(parents=True, exist_ok=True)
    args.md_out.write_text(md_text)
    logger.info("wrote markdown to %s", args.md_out)

    args.html_out.parent.mkdir(parents=True, exist_ok=True)
    args.html_out.write_text(_render_html(md_text))
    logger.info("wrote html to %s", args.html_out)
    print(f"wrote {args.md_out} and {args.html_out}")


def _load(parquet: Path) -> pl.DataFrame:
    df = pl.read_parquet(parquet)
    before = df.height
    df = df.filter(pl.col("player") != _LEFT_LEAGUE)
    logger.info(
        "loaded %d rows from %s (dropped %d submitted by %s)",
        df.height,
        parquet,
        before - df.height,
        _LEFT_LEAGUE,
    )
    return df


def _build_sections(df: pl.DataFrame, *, heatmap: Path) -> list[Section]:
    return [
        _section_overview(df),
        _section_best_players(df),
        _section_league_winners(df),
        _section_medal_table(df),
        _section_biggest_fans(df),
        _section_biggest_haters(df),
        _section_fan_hater_heatmap(heatmap),
        # song-focused sections grouped together
        _section_top_songs(df),
        _section_bottom_songs(df),
        _section_polarising_songs(df),
        _section_top_artists(df),
        _section_repeated_songs(df),
        _section_forfeits(df),
    ]


def _compile_markdown(sections: list[Section]) -> str:
    body = "\n\n".join(s.to_md() for s in sections)
    return f"# Music League analysis\n\n{body}\n"


def _parse_args() -> Args:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--parquet", type=Path, default=_DEFAULT_INPUT)
    p.add_argument("--md", dest="md_out", type=Path, default=_DEFAULT_OUTPUT_MD)
    p.add_argument("--html", dest="html_out", type=Path, default=_DEFAULT_OUTPUT_HTML)
    p.add_argument("--heatmap", dest="heatmap_out", type=Path, default=_DEFAULT_HEATMAP)
    p.add_argument("--log", type=Path, default=_DEFAULT_LOG)
    ns = p.parse_args()
    return Args(
        parquet=ns.parquet,
        md_out=ns.md_out,
        html_out=ns.html_out,
        heatmap_out=ns.heatmap_out,
        log=ns.log,
    )


def _section_overview(df: pl.DataFrame) -> Section:
    voters = _explode_votes(df).filter(pl.col("voter").is_not_null())["voter"].n_unique()
    table = pl.DataFrame(
        {
            "metric": [
                "Leagues",
                "Rounds",
                "Songs submitted",
                "Distinct submitters",
                "Distinct voters",
            ],
            "value": [
                df["league"].n_unique(),
                df.select(pl.col("round_id").n_unique()).item(),
                df.height,
                df["player"].n_unique(),
                voters,
            ],
        }
    )
    return Section(title="Overview", header=None, table=table, rank=False)


def _player_averages(df: pl.DataFrame) -> pl.DataFrame:
    return (
        _songs_with_round_zscore(df)
        .group_by("player")
        .agg(
            pl.col("z_in_round").mean().round(2).alias("avg_z"),
            pl.col("z_in_round").sum().round(2).alias("total_z"),
            pl.col("score").sum().alias("total_score"),
            pl.len().alias("songs"),
        )
        .filter(pl.col("songs") >= 2)  # one-shot submitters skew the leaderboard
        .sort("avg_z", descending=True)
    )


_PLAYER_AVG_HEADER = (
    "Players with at least 2 songs submitted, ranked by mean within-round z-score "
    "(score normalised against the other songs in the same round). avg_z > 0 means "
    "the player typically beats the round average; total_score is the raw points sum."
)


def _section_best_players(df: pl.DataFrame) -> Section:
    return Section(
        title="Player Ranking",
        header=_PLAYER_AVG_HEADER,
        table=_player_averages(df),
    )


def _songs_with_round_zscore(df: pl.DataFrame) -> pl.DataFrame:
    """One row per song with ``z_in_round = (score - round_mean) / round_std``.

    Rounds where every song scored identically (``round_std == 0``) are
    dropped — z-score is undefined and the row carries no information.
    """
    round_stats = df.group_by(["league", "round"]).agg(
        pl.col("score").mean().round(2).alias("round_avg"),
        pl.col("score").std(ddof=0).alias("round_std"),
    )
    return (
        df.join(round_stats, on=["league", "round"], how="inner")
        .filter(pl.col("round_std") > 0)
        .with_columns(
            ((pl.col("score") - pl.col("round_avg")) / pl.col("round_std"))
            .round(2)
            .alias("z_in_round"),
        )
    )


def _section_top_songs(df: pl.DataFrame) -> Section:
    table = (
        _songs_with_round_zscore(df)
        .sort("z_in_round", descending=True)
        .head(_TOP_N)
        .select(["z_in_round", "score", "round_avg", "song", "artist", "player", "league", "round"])
    )
    return Section(
        title="Over Performers",
        header=(
            f"Top {_TOP_N} songs ranked by how many standard deviations above the "
            "round average they scored — a 10 in a round averaging 4 outranks a 10 "
            "in a round averaging 8."
        ),
        table=table,
    )


def _section_bottom_songs(df: pl.DataFrame) -> Section:
    table = (
        _songs_with_round_zscore(df)
        .sort("z_in_round")
        .head(_TOP_N)
        .select(["z_in_round", "score", "round_avg", "song", "artist", "player", "league", "round"])
    )
    return Section(
        title="Under Performers",
        header=(
            f"Top {_TOP_N} songs ranked by how many standard deviations below the "
            "round average they scored. The score column is still the raw points; "
            "round_avg is the mean across all songs in that round."
        ),
        table=table,
    )


def _section_top_artists(df: pl.DataFrame) -> Section:
    table = (
        df.group_by("artist")
        .agg(
            pl.len().alias("plays"),
            pl.col("score").sum().alias("total_score"),
            pl.col("score").mean().round(2).alias("avg_score"),
        )
        .sort(["plays", "total_score"], descending=[True, True])
        .head(_TOP_N)
    )
    return Section(
        title="Most Played Artists",
        header=f"Top {_TOP_N} artists by number of songs submitted across all rounds.",
        table=table,
    )


def _section_league_winners(df: pl.DataFrame) -> Section:
    totals = df.group_by(["league", "player"]).agg(
        pl.col("score").sum().alias("total"),
        pl.len().alias("songs"),
    )
    table = (
        totals.sort(["league", "total"], descending=[False, True])
        .group_by("league", maintain_order=True)
        .head(1)
        .select(["league", "player", "total", "songs"])
    )
    return Section(
        title="League Winners",
        header="Player with the highest total score in each league.",
        table=table,
        rank=False,
    )


def _vote_z_scores(df: pl.DataFrame) -> pl.DataFrame:
    """Annotate every (voter, round, song) ballot with its z-score within the
    voter's votes that round.

    z = (vote - voter_mean_in_round) / voter_std_in_round.

    This normalises away differences in vote budget and voter generosity:
    a -1 stands out more if the voter only spread between 0 and +3 than if
    they were already swinging between +5 and -2. Rounds where the voter
    cast every vote at the same value (``std == 0``) are dropped — z is
    undefined and they carry no signal.
    """
    ballots = _explode_votes(df).filter(pl.col("voter").is_not_null())
    voter_round_stats = ballots.group_by(["league", "round", "voter"]).agg(
        pl.col("vote_count").mean().alias("voter_mean"),
        pl.col("vote_count").std(ddof=0).alias("voter_std"),
    )
    return (
        ballots.join(voter_round_stats, on=["league", "round", "voter"], how="inner")
        .filter(pl.col("voter_std") > 0)
        .with_columns(
            ((pl.col("vote_count") - pl.col("voter_mean")) / pl.col("voter_std")).alias("z"),
        )
    )


def _pair_z_summary(df: pl.DataFrame) -> pl.DataFrame:
    """Per (submitter, voter) pair: mean z-score, total points, shared rounds."""
    return (
        _vote_z_scores(df)
        .group_by(["player", "voter"])
        .agg(
            pl.col("z").mean().round(2).alias("avg_z"),
            pl.col("vote_count").sum().alias("total_points"),
            pl.len().alias("shared_rounds"),
        )
    )


_FAN_HATER_HEADER = (
    "For each submitter, the voter whose votes land furthest from that voter's own "
    "per-round vote distribution. Metric: mean z-score across shared rounds, where "
    "z = (vote - voter_round_mean) / voter_round_std and unrated songs in a "
    "participated round count as 0. Rounds where the voter gave every song the same "
    "vote are dropped (z is undefined). pts is the raw cumulative points for "
    "context. See the 'Fan / Hater Heatmap' for the full pair-by-pair view."
)


def _section_biggest_fans(df: pl.DataFrame) -> Section:
    table = (
        _pair_z_summary(df)
        .sort(["player", "avg_z"], descending=[False, True])
        .group_by("player", maintain_order=True)
        .head(1)
        .select(["player", "voter", "avg_z", "total_points", "shared_rounds"])
        .rename({"voter": "biggest_fan", "avg_z": "fan_z", "total_points": "pts"})
        .sort("fan_z", descending=True)
        .head(_FAN_HATER_PLAYERS)
    )
    return Section(title="Biggest Fans", header=_FAN_HATER_HEADER, table=table)


def _section_biggest_haters(df: pl.DataFrame) -> Section:
    table = (
        _pair_z_summary(df)
        .sort(["player", "avg_z"], descending=[False, False])
        .group_by("player", maintain_order=True)
        .head(1)
        .select(["player", "voter", "avg_z", "total_points", "shared_rounds"])
        .rename({"voter": "biggest_hater", "avg_z": "hater_z", "total_points": "pts"})
        .sort("hater_z")
        .head(_FAN_HATER_PLAYERS)
    )
    return Section(title="Biggest Haters", header=_FAN_HATER_HEADER, table=table)


def _section_fan_hater_heatmap(image: Path) -> Section:
    return Section(
        title="Fan / Hater Heatmap",
        header=(
            "Mean z-score per (submitter row, voter column) pair. Green = the voter "
            "tends to give that submitter higher-than-average votes (fan); red = "
            "lower-than-average (hater). Diagonal blank: nobody votes on their own "
            "song. Names alphabetised on both axes."
        ),
        image=image,
    )


_POLARISING_MIN_RATERS = 4


def _section_polarising_songs(df: pl.DataFrame) -> Section:
    """Songs that genuinely split the room.

    Per song we compute the population std of explicit (non-zero) votes, then
    z-score it against the other songs' stds in the same round. The song must
    have ``>=_POLARISING_MIN_RATERS`` explicit raters AND at least one positive
    AND at least one negative explicit vote — a standout +N alone is a
    consensus winner, not polarisation. Downvote-off leagues never qualify
    (no way to express dislike).
    """
    explicit = (
        _explode_votes(df).filter(pl.col("voter").is_not_null()).filter(pl.col("vote_count") != 0)
    )
    keys = ["league", "round", "player"]
    song_stats = (
        explicit.group_by(keys)
        .agg(
            pl.col("vote_count").std(ddof=0).alias("s"),
            pl.len().alias("n_raters"),
            (pl.col("vote_count") > 0).sum().alias("up_votes"),
            (pl.col("vote_count") < 0).sum().alias("down_votes"),
            pl.col("vote_count").filter(pl.col("vote_count") > 0).sum().alias("total_up"),
            (-pl.col("vote_count").filter(pl.col("vote_count") < 0).sum()).alias("total_down"),
        )
        .filter(pl.col("n_raters") >= _POLARISING_MIN_RATERS)
        .filter((pl.col("up_votes") >= 1) & (pl.col("down_votes") >= 1))
    )
    round_stats = (
        song_stats.group_by(["league", "round"])
        .agg(
            pl.col("s").mean().alias("round_mean_std"),
            pl.col("s").std(ddof=0).alias("round_std_of_std"),
        )
        .filter(pl.col("round_std_of_std") > 0)
    )
    songs = df.select([*keys, "song", "artist", "score"]).unique()
    table = (
        song_stats.join(round_stats, on=["league", "round"], how="inner")
        .with_columns(
            ((pl.col("s") - pl.col("round_mean_std")) / pl.col("round_std_of_std"))
            .round(2)
            .alias("z")
        )
        .join(songs, on=keys, how="inner")
        .sort("z", descending=True)
        .head(_TOP_N)
        .select(
            [
                "z",
                "score",
                "total_up",
                "total_down",
                "up_votes",
                "down_votes",
                "song",
                "artist",
                "player",
                "league",
                "round",
            ]
        )
    )
    return Section(
        title="Polarising Songs",
        header=(
            f"Top {_TOP_N} songs that genuinely split the room. Metric: per song, "
            "the std of its explicit (non-zero) votes, z-scored against the other "
            "songs' stds in the same round. Songs need at least "
            f"{_POLARISING_MIN_RATERS} explicit raters AND at least one positive "
            "AND at least one negative vote — a standout +N alone is a consensus "
            "winner, not polarisation. Leagues without downvotes are excluded by "
            "construction (no way to express dislike). total_up / total_down are "
            "the sums of positive / |negative| points; up_votes / down_votes are "
            "the head-counts."
        ),
        table=table,
    )


def _section_forfeits(df: pl.DataFrame) -> Section:
    table = (
        _explode_votes(df)
        .filter(pl.col("voter").is_null())
        .group_by("player")
        .agg(
            pl.len().alias("songs_with_forfeit"),
            pl.col("vote_count").sum().alias("total_forfeit_points"),
        )
        .sort("total_forfeit_points", descending=True)
    )
    return Section(
        title="Forfeits",
        header=(
            "Points lost on a player's songs when voters in that round failed to "
            "cast a ballot. Music League discards votes given by anyone who missed "
            "the voting deadline."
        ),
        table=table,
    )


_MEDAL_POINTS = {1: 3, 2: 2, 3: 1}


def _section_medal_table(df: pl.DataFrame) -> Section:
    """Olympic-style ranking: 3 points for a gold (1st in a round), 2 silver, 1 bronze.

    Ties share the higher rank — two songs tied for 1st both score 3 medal
    points; the next song slots in at rank 3 (bronze).
    """
    ranked = df.with_columns(
        pl.col("score")
        .rank(method="min", descending=True)
        .over(["league", "round"])
        .alias("round_rank")
    )
    medal_points_expr = (
        pl.when(pl.col("round_rank") == 1)
        .then(_MEDAL_POINTS[1])
        .when(pl.col("round_rank") == 2)
        .then(_MEDAL_POINTS[2])
        .when(pl.col("round_rank") == 3)
        .then(_MEDAL_POINTS[3])
        .otherwise(0)
        .alias("medal_points")
    )
    table = (
        ranked.with_columns(medal_points_expr)
        .group_by("player")
        .agg(
            (pl.col("round_rank") == 1).sum().alias("gold 🥇"),
            (pl.col("round_rank") == 2).sum().alias("silver 🥈"),
            (pl.col("round_rank") == 3).sum().alias("bronze 🥉"),
            pl.col("medal_points").sum().alias("medal_points"),
        )
        .sort(
            ["medal_points", "gold 🥇", "silver 🥈", "bronze 🥉"],
            descending=[True, True, True, True],
        )
    )
    return Section(
        title="Medal Ranking",
        header=(
            "Olympic-style: 3 points for finishing 1st in a round, 2 for 2nd, 1 for "
            "3rd. Ties share the higher rank, so two songs tied for 1st both earn "
            "3 medal points."
        ),
        table=table,
    )


def _section_repeated_songs(df: pl.DataFrame) -> Section:
    """Tracks submitted to more than one round (across all leagues)."""
    table = (
        df.group_by("spotify_track_id")
        .agg(
            pl.col("song").first(),
            pl.col("artist").first(),
            pl.len().alias("plays"),
            pl.col("player").unique().sort().str.join(", ").alias("players"),
            pl.col("score").sum().alias("total_score"),
        )
        .filter(pl.col("plays") > 1)
        .sort(["plays", "total_score"], descending=[True, True])
        .select(["plays", "song", "artist", "players", "total_score"])
    )
    return Section(
        title="Repeats",
        header=(
            "Tracks (matched by Spotify track ID) submitted in more than one round, "
            "either by the same player or by different players."
        ),
        table=table,
    )


def _explode_votes(df: pl.DataFrame) -> pl.DataFrame:
    """One row per (song x voter), with implicit zero-votes filled in.

    Music League's HTML only lists voters who gave a non-zero vote on a song,
    so the raw scrape misses the rounds where a voter participated but rated
    a particular song 0. Without those rows the per-(voter, round) mean and
    std are biased upward, the shared_rounds count understates real round
    overlap, and a z-score-based fan/hater is too easy to mint.

    This function rebuilds the full ballot:
      - ``participants[round]`` = the union of non-null voters across every
        song in that round (anyone who showed up at all).
      - For each (round, voter), every song in that round becomes a row,
        excluding the voter's own song (you cannot vote for yourself).
      - vote_count is whatever the scrape recorded, else 0.

    The forfeit-bucket ``None`` voter rows are passed through unchanged —
    they are aggregate accounting, not ballots.
    """
    base = (
        df.select(["league", "round", "player", "score", "votes"])
        .explode("votes")
        .with_columns(
            pl.col("votes").struct.field("voter").alias("voter"),
            pl.col("votes").struct.field("votes").alias("vote_count"),
        )
        .drop("votes")
        .filter(pl.col("vote_count").is_not_null())
        .filter((pl.col("voter") != _LEFT_LEAGUE) | pl.col("voter").is_null())
    )
    forfeits = base.filter(pl.col("voter").is_null())
    real = base.filter(pl.col("voter").is_not_null())

    songs = df.select(["league", "round", "player", "score"]).unique()
    participants = real.select(["league", "round", "voter"]).unique()
    filled = (
        participants.join(songs, on=["league", "round"], how="inner")
        .filter(pl.col("voter") != pl.col("player"))
        .join(
            real.select(["league", "round", "player", "voter", "vote_count"]),
            on=["league", "round", "player", "voter"],
            how="left",
        )
        .with_columns(pl.col("vote_count").fill_null(0))
        .select(["league", "round", "player", "score", "voter", "vote_count"])
    )
    return pl.concat([filled, forfeits], how="vertical")


def _with_rank(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_row_index("rank", offset=1)


def _md_table(df: pl.DataFrame) -> str:
    if df.height == 0:
        return "_(no rows)_"
    return tabulate(df.iter_rows(), headers=df.columns, tablefmt="github")


def _render_fan_hater_heatmap(df: pl.DataFrame, out_path: Path) -> None:
    """Save a square avg-z heatmap (submitter rows x voter cols) to ``out_path``.

    Cells are annotated with their z-score; the diagonal is blank (no
    self-voting). Names are alphabetised on both axes. Diverging colormap
    (RdYlGn) is centred on 0 so positive z stays green and negative red
    regardless of the data range.
    """
    pairs = _pair_z_summary(df)
    names = sorted({*df["player"].to_list(), *pairs["voter"].to_list()})
    n = len(names)
    idx = {name: i for i, name in enumerate(names)}

    matrix = np.full((n, n), np.nan)
    for row in pairs.iter_rows(named=True):
        matrix[idx[row["player"]], idx[row["voter"]]] = row["avg_z"]

    finite = matrix[~np.isnan(matrix)]
    bound = float(np.nanmax(np.abs(finite))) if finite.size else 1.0
    norm = TwoSlopeNorm(vmin=-bound, vcenter=0.0, vmax=bound)

    fig, ax = plt.subplots(figsize=(0.7 * n + 2, 0.7 * n + 2))
    img = ax.imshow(matrix, cmap="RdYlGn", norm=norm, aspect="equal")
    ax.set_xticks(range(n), names, rotation=45, ha="right")
    ax.set_yticks(range(n), names)
    ax.set_xlabel("voter")
    ax.set_ylabel("submitter")
    ax.set_title("Fan / Hater heatmap (avg z-score)")

    for i in range(n):
        for j in range(n):
            value = matrix[i, j]
            if np.isnan(value):
                continue
            # White text on dark cells, black on light — pick by colormap luminance.
            rgba = img.cmap(img.norm(value))
            luminance = 0.2126 * rgba[0] + 0.7152 * rgba[1] + 0.0722 * rgba[2]
            colour = "white" if luminance < 0.5 else "black"
            ax.text(j, i, f"{value:.2f}", ha="center", va="center", color=colour, fontsize=8)

    fig.colorbar(img, ax=ax, shrink=0.7, label="avg z-score")
    fig.tight_layout()
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def _render_html(md_text: str) -> str:
    body = markdown.markdown(md_text, extensions=["tables"])
    return _HTML_TEMPLATE.format(body=body)


_HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Music League analysis</title>
<style>
 body {{
   font-family: system-ui, sans-serif;
   max-width: 60rem;
   margin: 2rem auto;
   padding: 0 1rem;
   line-height: 1.45;
 }}
 h1, h2, h3 {{ border-bottom: 1px solid #ddd; padding-bottom: .25rem; }}
 table {{ border-collapse: collapse; margin: 1rem 0; }}
 th, td {{ border: 1px solid #ccc; padding: .35rem .6rem; text-align: left; }}
 th {{ background: #f4f4f4; }}
 tr:nth-child(even) {{ background: #fafafa; }}
 code {{ background: #f4f4f4; padding: .1rem .3rem; border-radius: 3px; }}
</style>
</head>
<body>
{body}
</body>
</html>
"""


if __name__ == "__main__":
    main()
