"""Anonymise display names by collapsing space-separated names to
``FirstName LastInitial``.

Single-word handles (e.g. ``harryg``) are left untouched. When two players
share the same first name, the last-name prefix is extended until each
short form is unique (e.g. ``Sam Mitchell`` / ``Sam Milburn`` →
``Sam Mit`` / ``Sam Mil``).
"""

from __future__ import annotations

import logging
from collections.abc import Iterable

import polars as pl

logger = logging.getLogger(__name__)

_VOTES_DTYPE = pl.List(pl.Struct({"voter": pl.Utf8, "votes": pl.Int64}))


def build_short_name_map(names: Iterable[str]) -> dict[str, str]:
    """Return ``{full_name: short_name}`` for every multi-word name in ``names``.

    Names without a space are not included in the map (callers should leave
    those untouched). Within a first-name group, the last-name prefix is
    grown one character at a time until every short form is distinct.
    """
    by_first: dict[str, list[tuple[str, str]]] = {}
    for full in {n for n in names if _looks_like_real_name(n)}:
        first, *rest = full.split(" ")
        last = " ".join(rest)
        by_first.setdefault(first, []).append((full, last))

    short: dict[str, str] = {}
    for first, entries in by_first.items():
        prefix_len = _min_unique_prefix(last for _, last in entries)
        for full, last in entries:
            short[full] = f"{first} {last[:prefix_len]}"
    return short


def _looks_like_real_name(name: object) -> bool:
    """A real first+last name has a space and no bracket/punctuation noise.

    Excludes Music League's ``[Left the league]`` placeholder and any other
    bracketed/templated string the site might use.
    """
    if not isinstance(name, str):
        return False
    stripped = name.strip()
    if " " not in stripped:
        return False
    if stripped.startswith("[") or stripped.endswith("]"):
        return False
    return True


def _min_unique_prefix(values: Iterable[str]) -> int:
    pool = list(values)
    if len(set(pool)) <= 1:
        return 1
    longest = max(len(v) for v in pool)
    for n in range(1, longest + 1):
        if len({v[:n] for v in pool}) == len(pool):
            return n
    return longest


def anonymise_dataframe(df: pl.DataFrame) -> pl.DataFrame:
    """Replace ``player`` and ``votes[*].voter`` with their short forms."""
    voters = (
        df.select(pl.col("votes").explode().struct.field("voter"))
        .drop_nulls()
        .to_series()
        .unique()
        .to_list()
    )
    players = df["player"].unique().to_list()
    short = build_short_name_map(players + voters)
    if not short:
        return df
    logger.info("anonymising %d distinct full names", len(short))

    return df.with_columns(
        pl.col("player").replace(short),
        pl.col("votes")
        .list.eval(
            pl.struct(
                pl.element().struct.field("voter").replace(short).alias("voter"),
                pl.element().struct.field("votes").alias("votes"),
            )
        )
        .cast(_VOTES_DTYPE),
    )
