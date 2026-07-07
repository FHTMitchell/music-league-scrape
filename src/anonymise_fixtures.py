#!/usr/bin/env python3
"""Anonymise saved Music League HTML into shareable test fixtures.

Real result pages (as dumped by ``scrape --debug`` into ``debug/``) carry
personal data: player/voter display names, free-text vote comments, and
user-id hashes / avatar URLs. This script scrubs all of that and writes clean
copies into ``webpages/`` for use as offline parser fixtures.

No real names are stored in this file. The script discovers the real names in
the input pages, sorts them, and indexes them into a generated pool of
fictional names: the *i*-th distinct real name (alphabetically) becomes the
*i*-th fake name. The same real name maps to the same fake name across every
processed page, so a person is anonymised consistently everywhere.

League/round IDs are left untouched (they are public URL identifiers the parser
tests assert on); only ``/user/{id}/`` and avatar-asset user IDs are scrubbed.
Song titles, artists and league names are left untouched (public track data).

The final fake names actually placed into each fixture are written to
``tests/fixture_names.json`` so the parser tests can assert against them without
hardcoding either the real or the generated names.

Usage:
    python -m src.anonymise_fixtures IN.html:OUT.html [IN.html:OUT.html ...]
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from selectolax.parser import HTMLParser, Node

from src.log import install as install_logger

logger = logging.getLogger(__name__)

_DEFAULT_LOG = Path("logs/anonymise_fixtures.log")
_NAMES_OUT = Path("tests/fixture_names.json")

# Fictional pools, alphabetised. Real names index into these by sorted position;
# separate pools keep the "real name" (has a space) vs "single-word handle"
# distinction that src/names.py relies on. Extend if a page has more distinct
# names than a pool holds — the script errors out rather than reuse a name.
_FAKE_FULL_NAMES = sorted(
    [
        "Alex Carter",
        "Blair Nolan",
        "Casey Dunn",
        "Devon Marsh",
        "Elliot Frey",
        "Frankie Hale",
        "Greer Landry",
        "Harley Voss",
        "Indira Sol",
        "Jules Reyes",
        "Kai Bramble",
        "Lennox Doyle",
        "Marlow Pike",
        "Nova Ellery",
        "Ocean Trent",
        "Perry Vance",
        "Quinn Ashby",
        "Reese Calloway",
        "Sage Winters",
        "Tatum Brooks",
    ]
)
_FAKE_HANDLES = sorted(
    [
        "amberwave",
        "bluefox",
        "cinderpost",
        "driftwood",
        "emberlark",
        "frostwren",
        "glassvine",
        "hollowtide",
        "ionridge",
        "jadeloop",
        "kelpstorm",
        "lumenbat",
        "mossgleam",
        "nettleash",
        "opaldrift",
        "pineglow",
    ]
)

# Innocuous stand-ins, cycled so real vote comments never leak.
_FAKE_COMMENTS = [
    "Great pick.",
    "Not for me but I get it.",
    "Solid choice for the theme.",
    "Grew on me by the end.",
    "Classic.",
    "Bit of a slow burn.",
    "Instant upvote.",
    "Missed the mark for me.",
]

_VOTER_SEL = "b.d-block.text-truncate.text-body"
_RANK_CARD_SEL = 'div.card.mt-3[class*="rank-"]'
_SUBMITTER_SEL = "h6.text-body.fw-semibold"
_COMMENT_SEL = "span.text-break.ws-pre-wrap"

# Inner text of a voter <b> or submitter <h6> tag (used for replacement).
# Tags may carry extra attributes (e.g. style=) after the class, so allow any
# attributes up to the closing '>'.
_VOTER_TAG = re.compile(r'(<b class="d-block text-truncate text-body[^"]*"[^>]*>)([^<]*)(</b>)')
_SUBMITTER_TAG = re.compile(r'(<h6 class="[^"]*\bfw-semibold\b[^"]*"[^>]*>)([^<]*)(</h6>)')
_COMMENT_TAG = re.compile(r'(<span class="[^"]*\bws-pre-wrap\b[^"]*"[^>]*>)([^<]*)(</span>)')
_USER_ID = re.compile(r"(/users?/)([0-9a-f]{32})")
# Names also appear on avatar tooltips and in inlined JSON blobs.
_TITLE_ATTR = re.compile(r'(title=")([^"]*)(")')
_JSON_NAME = re.compile(r"(&quot;name&quot;:&quot;)([^&]*)(&quot;)")


@dataclass(frozen=True)
class Job:
    src: Path
    dst: Path


def main() -> None:
    args = _parse_args()
    install_logger(args.log)

    pages = {job: job.src.read_text() for job in args.jobs}

    # One global mapping across every page so a person is scrubbed identically.
    full_names, handles = _collect_names(pages.values())
    name_map = _build_name_map(full_names, _FAKE_FULL_NAMES, "full name")
    name_map |= _build_name_map(handles, _FAKE_HANDLES, "handle")
    logger.info("mapping %d distinct names", len(name_map))

    manifest: dict[str, dict] = {}
    for job, html in pages.items():
        cleaned, page_manifest = _anonymise(html, name_map)
        _assert_scrubbed(cleaned, name_map)
        job.dst.parent.mkdir(parents=True, exist_ok=True)
        job.dst.write_text(cleaned)
        manifest[job.dst.name] = page_manifest
        logger.info(
            "wrote %s -> %s (%d names, %d comments)",
            job.src,
            job.dst,
            len(page_manifest["names"]),
            page_manifest["n_comments"],
        )
        print(f"anonymised {job.src} -> {job.dst}")

    _NAMES_OUT.parent.mkdir(parents=True, exist_ok=True)
    _NAMES_OUT.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"wrote fixture manifest to {_NAMES_OUT}")


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("pairs", nargs="+", metavar="IN:OUT", help="input:output HTML pairs")
    p.add_argument("--log", type=Path, default=_DEFAULT_LOG)
    ns = p.parse_args()
    jobs = []
    for pair in ns.pairs:
        src, _, dst = pair.partition(":")
        if not src or not dst:
            p.error(f"expected IN:OUT, got {pair!r}")
        jobs.append(Job(Path(src), Path(dst)))
    ns.jobs = jobs
    return ns


def _text(node: Node) -> str:
    return (node.text(deep=False) or "").strip()


def _collect_names(pages) -> tuple[list[str], list[str]]:  # noqa: ANN001
    """Return (sorted full names, sorted handles) across all pages."""
    full: set[str] = set()
    handles: set[str] = set()
    for html in pages:
        tree = HTMLParser(html)
        names = {_text(n) for n in tree.css(_VOTER_SEL)}
        for card in tree.css(_RANK_CARD_SEL):
            sub = card.css_first(_SUBMITTER_SEL)
            if sub is not None:
                names.add(_text(sub))
        for name in names:
            if not name or name.startswith("["):  # skip "[Left the league]"
                continue
            (full if " " in name else handles).add(name)
    return sorted(full), sorted(handles)


def _build_name_map(reals: list[str], pool: list[str], kind: str) -> dict[str, str]:
    if len(reals) > len(pool):
        sys.exit(f"need {len(reals)} fake {kind}s but pool has {len(pool)}; extend the pool")
    return dict(zip(reals, pool))


def _anonymise(html: str, name_map: dict[str, str]) -> tuple[str, dict]:
    """Scrub names, comments and user-ids from ``html``.

    Returns the cleaned HTML and a manifest of the fake values it now contains
    (``{"names": [...], "comments": [...]}``) so tests can assert against them.
    """
    present: set[str] = set()
    placed_comments: list[str] = []

    def rename(m: re.Match[str]) -> str:
        real = m.group(2).strip()
        fake = name_map.get(real)
        if fake is None:
            return m.group(0)  # not a name (e.g. "6 voters", "Album art")
        present.add(fake)
        return f"{m.group(1)}{fake}{m.group(3)}"

    def decomment(m: re.Match[str]) -> str:
        if not m.group(2).strip():
            return m.group(0)  # keep empty comment spans empty
        fake = _FAKE_COMMENTS[len(placed_comments) % len(_FAKE_COMMENTS)]
        placed_comments.append(fake)
        return f"{m.group(1)}{fake}{m.group(3)}"

    html = _VOTER_TAG.sub(rename, html)
    html = _SUBMITTER_TAG.sub(rename, html)
    html = _TITLE_ATTR.sub(rename, html)  # avatar tooltips; "Album art" etc. pass through
    html = _JSON_NAME.sub(rename, html)  # inlined JSON name fields
    html = _COMMENT_TAG.sub(decomment, html)
    html = _USER_ID.sub(lambda m: f"{m.group(1)}{'0' * 32}", html)
    manifest = {"names": sorted(present), "n_comments": len(placed_comments)}
    return html, manifest


def _assert_scrubbed(html: str, name_map: dict[str, str]) -> None:
    """Fail loudly if any real name survived, so gaps are never shipped."""
    leaked = sorted(real for real in name_map if real in html)
    if leaked:
        sys.exit(f"anonymisation incomplete, real names still present: {leaked}")


if __name__ == "__main__":
    main()
