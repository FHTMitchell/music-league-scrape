"""Anonymise display names by collapsing space-separated names to
``FirstName LastInitial``.

Single-word handles are left untouched. When two players share the same
first name, the last-name prefix is extended until each short form is
unique (e.g. ``Pat Brown`` / ``Pat Briggs`` → ``Pat Bro`` / ``Pat Bri``).
"""

from __future__ import annotations

import json
import logging
from collections.abc import Iterable
from pathlib import Path

import polars as pl

logger = logging.getLogger(__name__)

_VOTES_DTYPE = pl.List(pl.Struct({"voter": pl.Utf8, "votes": pl.Int64}))


def load_name_overrides(path: Path) -> dict[str, str]:
    """Load ``{raw_name: display_name}`` overrides from a JSON file.

    Returns an empty mapping if the file does not exist, so overrides are
    entirely optional. Applied to both ``player`` and ``votes[*].voter``.
    """
    if not path.is_file():
        logger.debug("no name-overrides file at %s; skipping", path)
        return {}
    overrides = json.loads(path.read_text())
    logger.info("loaded %d name overrides from %s", len(overrides), path)
    return overrides


def apply_name_overrides(df: pl.DataFrame, overrides: dict[str, str]) -> pl.DataFrame:
    """Replace ``player`` and ``votes[*].voter`` names using ``overrides``."""
    if not overrides:
        return df
    return df.with_columns(
        pl.col("player").replace(overrides),
        pl.col("votes")
        .list.eval(
            pl.struct(
                pl.element().struct.field("voter").replace(overrides).alias("voter"),
                pl.element().struct.field("votes").alias("votes"),
            )
        )
        .cast(_VOTES_DTYPE),
    )


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
