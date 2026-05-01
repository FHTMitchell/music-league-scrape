"""Render every song in ``out/music_league.parquet`` as a self-contained
``out/songs.html`` page with a client-side search-by-title box.

The data is embedded inline as JSON so the page works from ``file://`` (no
server needed). For ~500 rows the resulting HTML is well under 200 KB.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

import polars as pl

from src.log import install as install_logger

logger = logging.getLogger(__name__)

_DEFAULT_INPUT = Path("out/music_league.parquet")
_DEFAULT_OUTPUT = Path("out/songs.html")
_DEFAULT_LOG = Path("logs/songs_page.log")
_LEFT_LEAGUE = "[Left the league]"
_COLUMNS = ("score", "song", "artist", "player", "league", "round", "round_time")


@dataclass(frozen=True)
class Args:
    parquet: Path
    out: Path
    log: Path


def main() -> None:
    args = _parse_args()
    install_logger(args.log)

    if not args.parquet.exists():
        sys.exit(
            f"{args.parquet} not found. Run the scraper first:\n    uv run python -m src.scrape\n"
        )

    df = (
        pl.read_parquet(args.parquet)
        .filter(pl.col("player") != _LEFT_LEAGUE)
        .sort("round_time", descending=True)
        .with_columns(pl.col("round_time").dt.strftime("%Y-%m-%d").alias("round_time"))
        .select(_COLUMNS)
    )
    rows = df.to_dicts()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(_render_html(rows))
    logger.info("wrote %d rows to %s", len(rows), args.out)
    print(f"wrote {args.out} ({len(rows)} songs)")


def _parse_args() -> Args:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--parquet", type=Path, default=_DEFAULT_INPUT)
    p.add_argument("--out", type=Path, default=_DEFAULT_OUTPUT)
    p.add_argument("--log", type=Path, default=_DEFAULT_LOG)
    ns = p.parse_args()
    return Args(parquet=ns.parquet, out=ns.out, log=ns.log)


def _render_html(rows: list[dict]) -> str:
    return _PAGE.replace(
        "__SONGS_JSON__",
        json.dumps(rows, ensure_ascii=False, separators=(",", ":")),
    ).replace("__COUNT__", str(len(rows)))


_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Music League songs</title>
<style>
 body {
   font-family: system-ui, sans-serif;
   max-width: 80rem;
   margin: 2rem auto;
   padding: 0 1rem;
   line-height: 1.45;
 }
 h1 { border-bottom: 1px solid #ddd; padding-bottom: .25rem; }
 .toolbar { display: flex; gap: 1rem; align-items: center; margin: 1rem 0; }
 #search {
   flex: 1;
   font-size: 1rem;
   padding: .5rem .75rem;
   border: 1px solid #ccc;
   border-radius: 4px;
 }
 #count { color: #666; font-variant-numeric: tabular-nums; }
 table { border-collapse: collapse; width: 100%; }
 th, td { border: 1px solid #ccc; padding: .35rem .6rem; text-align: left; vertical-align: top; }
 th { background: #f4f4f4; position: sticky; top: 0; }
 tr:nth-child(even) td { background: #fafafa; }
 td.score { text-align: right; font-variant-numeric: tabular-nums; width: 4rem; }
 td.date { white-space: nowrap; color: #666; }
 .hidden { display: none; }
</style>
</head>
<body>
<h1>Music League songs</h1>
<div class="toolbar">
  <input id="search" type="search" placeholder="Filter by song title…" autofocus>
  <span id="count"></span>
</div>
<table>
  <thead>
    <tr>
      <th>Score</th><th>Song</th><th>Artist</th><th>Player</th>
      <th>League</th><th>Round</th><th>Date</th>
    </tr>
  </thead>
  <tbody id="rows"></tbody>
</table>
<script>
 const SONGS = __SONGS_JSON__;
 const TOTAL = __COUNT__;
 const tbody = document.getElementById("rows");
 const search = document.getElementById("search");
 const counter = document.getElementById("count");

 function escapeHtml(s) {
   return String(s ?? "").replace(/[&<>"]/g, c => (
     {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]
   ));
 }

 function render(filter) {
   const q = filter.trim().toLowerCase();
   const html = [];
   let shown = 0;
   for (const r of SONGS) {
     if (q && !r.song.toLowerCase().includes(q)) continue;
     shown++;
     html.push(
       "<tr>" +
       `<td class="score">${escapeHtml(r.score)}</td>` +
       `<td>${escapeHtml(r.song)}</td>` +
       `<td>${escapeHtml(r.artist)}</td>` +
       `<td>${escapeHtml(r.player)}</td>` +
       `<td>${escapeHtml(r.league)}</td>` +
       `<td>${escapeHtml(r.round)}</td>` +
       `<td class="date">${escapeHtml(r.round_time)}</td>` +
       "</tr>"
     );
   }
   tbody.innerHTML = html.join("");
   counter.textContent = q
     ? `${shown} / ${TOTAL} songs`
     : `${TOTAL} songs`;
 }

 search.addEventListener("input", e => render(e.target.value));
 render("");
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
