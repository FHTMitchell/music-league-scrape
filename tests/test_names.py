"""Tests for the name anonymiser."""

from __future__ import annotations

import polars as pl

from src.names import anonymise_dataframe, build_short_name_map

_VOTES_DTYPE = pl.List(pl.Struct({"voter": pl.Utf8, "votes": pl.Int64}))


def test_single_word_handles_are_left_alone() -> None:
    assert build_short_name_map(["alice99", "soloplayer", "Joe"]) == {}


def test_simple_first_last_collapses_to_first_initial() -> None:
    short = build_short_name_map(["Jane Doe", "John Smith"])
    assert short == {"Jane Doe": "Jane D", "John Smith": "John S"}


def test_collision_extends_prefix_until_unique() -> None:
    short = build_short_name_map(["Pat Brown", "Pat Briggs"])
    assert short == {"Pat Brown": "Pat Bro", "Pat Briggs": "Pat Bri"}


def test_bracketed_placeholder_is_excluded() -> None:
    """``[Left the league]`` looks like a multi-word name but is not one."""
    short = build_short_name_map(["[Left the league]", "Jane Doe"])
    assert "[Left the league]" not in short
    assert short["Jane Doe"] == "Jane D"


def test_three_way_first_name_collision_extends_to_min_unique() -> None:
    short = build_short_name_map(["Pat Brown", "Pat Briggs", "Pat Black"])
    assert short == {
        "Pat Brown": "Pat Bro",
        "Pat Briggs": "Pat Bri",
        "Pat Black": "Pat Bla",
    }


def test_anonymise_dataframe_replaces_player_and_voter_columns() -> None:
    df = pl.DataFrame(
        {
            "player": ["Jane Doe", "alice99"],
            "votes": [
                [{"voter": "Pat Brown", "votes": 3}, {"voter": "alice99", "votes": 1}],
                [{"voter": "Jane Doe", "votes": 2}, {"voter": None, "votes": -1}],
            ],
        },
        schema_overrides={"votes": _VOTES_DTYPE},
    )
    out = anonymise_dataframe(df)
    assert out["player"].to_list() == ["Jane D", "alice99"]
    voters = [[v["voter"] for v in row] for row in out["votes"].to_list()]
    assert voters == [["Pat B", "alice99"], ["Jane D", None]]


def test_anonymise_dataframe_idempotent() -> None:
    df = pl.DataFrame(
        {
            "player": ["Jane Doe"],
            "votes": [[{"voter": "Pat Brown", "votes": 3}]],
        },
        schema_overrides={"votes": _VOTES_DTYPE},
    )
    once = anonymise_dataframe(df)
    twice = anonymise_dataframe(once)
    assert once.equals(twice)
