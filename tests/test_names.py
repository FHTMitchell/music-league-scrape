"""Tests for the name anonymiser."""

from __future__ import annotations

import polars as pl

from src.names import anonymise_dataframe, build_short_name_map

_VOTES_DTYPE = pl.List(pl.Struct({"voter": pl.Utf8, "votes": pl.Int64}))


def test_single_word_handles_are_left_alone() -> None:
    assert build_short_name_map(["harryg", "Solsti", "Joe"]) == {}


def test_simple_first_last_collapses_to_first_initial() -> None:
    short = build_short_name_map(["Fred Norman", "Peter Lawrence"])
    assert short == {"Fred Norman": "Fred N", "Peter Lawrence": "Peter L"}


def test_collision_extends_prefix_until_unique() -> None:
    short = build_short_name_map(["Sam Mitchell", "Sam Milburn"])
    assert short == {"Sam Mitchell": "Sam Mit", "Sam Milburn": "Sam Mil"}


def test_bracketed_placeholder_is_excluded() -> None:
    """``[Left the league]`` looks like a multi-word name but is not one."""
    short = build_short_name_map(["[Left the league]", "Fred Norman"])
    assert "[Left the league]" not in short
    assert short["Fred Norman"] == "Fred N"


def test_three_way_first_name_collision_extends_to_min_unique() -> None:
    short = build_short_name_map(["Sam Mitchell", "Sam Milburn", "Sam Smith"])
    assert short == {
        "Sam Mitchell": "Sam Mit",
        "Sam Milburn": "Sam Mil",
        "Sam Smith": "Sam Smi",
    }


def test_anonymise_dataframe_replaces_player_and_voter_columns() -> None:
    df = pl.DataFrame(
        {
            "player": ["Fred Norman", "harryg"],
            "votes": [
                [{"voter": "Sam Mitchell", "votes": 3}, {"voter": "harryg", "votes": 1}],
                [{"voter": "Fred Norman", "votes": 2}, {"voter": None, "votes": -1}],
            ],
        },
        schema_overrides={"votes": _VOTES_DTYPE},
    )
    out = anonymise_dataframe(df)
    assert out["player"].to_list() == ["Fred N", "harryg"]
    voters = [[v["voter"] for v in row] for row in out["votes"].to_list()]
    assert voters == [["Sam M", "harryg"], ["Fred N", None]]


def test_anonymise_dataframe_idempotent() -> None:
    df = pl.DataFrame(
        {
            "player": ["Fred Norman"],
            "votes": [[{"voter": "Sam Mitchell", "votes": 3}]],
        },
        schema_overrides={"votes": _VOTES_DTYPE},
    )
    once = anonymise_dataframe(df)
    twice = anonymise_dataframe(once)
    assert once.equals(twice)
