"""Tests for the statistical pieces of the analysis module."""

from __future__ import annotations

import polars as pl

from src.analyze import _explode_votes, _player_averages, _vote_z_scores

_VOTES_DTYPE = pl.List(pl.Struct({"voter": pl.Utf8, "votes": pl.Int64}))


def _build_df(rows: list[dict]) -> pl.DataFrame:
    return pl.DataFrame(rows, schema_overrides={"votes": _VOTES_DTYPE})


def test_explode_votes_fills_implicit_zeros_for_participated_rounds() -> None:
    """A voter who rates one song in a round implicitly rates the others 0."""
    df = _build_df(
        [
            # Round R1: alice and bob each submit a song; charlie votes only on alice's
            {
                "league": "L",
                "round": "R1",
                "player": "alice",
                "score": 3,
                "votes": [{"voter": "charlie", "votes": 3}],
            },
            {
                "league": "L",
                "round": "R1",
                "player": "bob",
                "score": 0,
                "votes": [],
            },
        ]
    )
    out = _explode_votes(df).sort(["voter", "player"])
    rows = list(out.iter_rows(named=True))
    # charlie should have one explicit vote on alice and one implicit 0 on bob
    assert len(rows) == 2
    by_song = {r["player"]: r["vote_count"] for r in rows}
    assert by_song == {"alice": 3, "bob": 0}


def test_explode_votes_does_not_create_self_votes() -> None:
    """Submitters cannot vote on their own song."""
    df = _build_df(
        [
            {
                "league": "L",
                "round": "R1",
                "player": "alice",
                "score": 2,
                "votes": [{"voter": "bob", "votes": 2}],
            },
            {
                "league": "L",
                "round": "R1",
                "player": "bob",
                "score": 1,
                "votes": [{"voter": "alice", "votes": 1}],
            },
        ]
    )
    out = _explode_votes(df)
    self_votes = out.filter(pl.col("player") == pl.col("voter"))
    assert self_votes.height == 0


def test_explode_votes_preserves_forfeit_bucket() -> None:
    df = _build_df(
        [
            {
                "league": "L",
                "round": "R1",
                "player": "alice",
                "score": 5,
                "votes": [
                    {"voter": "bob", "votes": 3},
                    {"voter": None, "votes": 2},  # forfeit
                ],
            },
            {
                "league": "L",
                "round": "R1",
                "player": "bob",
                "score": 1,
                "votes": [{"voter": "alice", "votes": 1}],
            },
        ]
    )
    out = _explode_votes(df)
    forfeits = out.filter(pl.col("voter").is_null())
    assert forfeits.height == 1
    assert forfeits["vote_count"].item() == 2


def test_vote_z_scores_uses_implicit_zeros_in_voter_round_stats() -> None:
    """A voter's per-round mean/std should include the 0s on songs they ignored."""
    df = _build_df(
        [
            {
                "league": "L",
                "round": "R1",
                "player": "alice",
                "score": 4,
                "votes": [{"voter": "diana", "votes": 4}],
            },
            {
                "league": "L",
                "round": "R1",
                "player": "bob",
                "score": 0,
                "votes": [],
            },
            {
                "league": "L",
                "round": "R1",
                "player": "carol",
                "score": 0,
                "votes": [],
            },
            {
                "league": "L",
                "round": "R1",
                "player": "diana",
                "score": 0,
                "votes": [],
            },
        ]
    )
    z = _vote_z_scores(df)
    # Diana voted on 3 other songs: alice=4, bob=0, carol=0. mean=4/3 ~= 1.33,
    # std (population) = sqrt((4-4/3)^2 + 2*(0-4/3)^2) / sqrt(3) ~= 1.886.
    diana_alice = z.filter((pl.col("voter") == "diana") & (pl.col("player") == "alice"))["z"].item()
    assert abs(diana_alice - (4 - 4 / 3) / 1.8856180831641267) < 1e-6


def test_player_averages_excludes_one_shot_submitters() -> None:
    """Players with only a single song are dropped to keep the leaderboard sane."""
    df = _build_df(
        [
            {
                "league": "L",
                "round": "R1",
                "player": "veteran",
                "score": 5,
                "votes": [{"voter": "fan", "votes": 5}],
            },
            {
                "league": "L",
                "round": "R2",
                "player": "veteran",
                "score": 3,
                "votes": [{"voter": "fan", "votes": 3}],
            },
            {
                "league": "L",
                "round": "R1",
                "player": "fan",
                "score": 0,
                "votes": [],
            },
            {
                "league": "L",
                "round": "R2",
                "player": "fan",
                "score": 0,
                "votes": [],
            },
            {
                "league": "L",
                "round": "R3",
                "player": "newbie",
                "score": 1,
                "votes": [{"voter": "fan", "votes": 1}],
            },
            {
                "league": "L",
                "round": "R3",
                "player": "fan",
                "score": 0,
                "votes": [],
            },
        ]
    )
    avgs = _player_averages(df)
    assert "newbie" not in avgs["player"].to_list()
    assert "veteran" in avgs["player"].to_list()
