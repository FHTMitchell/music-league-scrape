"""Render every song in ``out/music_league.parquet`` as a self-contained
``out/songs.html`` page with a client-side search box (song title or artist).

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

from src.analyze import _with_round_zscores
from src.log import install as install_logger
from src.names import apply_name_overrides, load_name_overrides

logger = logging.getLogger(__name__)

_DEFAULT_INPUT = Path("out/music_league.parquet")
_DEFAULT_OUTPUT = Path("out/songs.html")
_DEFAULT_LOG = Path("logs/songs_page.log")
_DEFAULT_NAME_OVERRIDES = Path("name-overrides.json")
_LEFT_LEAGUE = "[Left the league]"
_Z_DP = 3  # decimal places for the displayed song z-score
_COLUMNS = ("score", "z_in_round", "song", "artist", "player", "league", "round", "round_time")


@dataclass(frozen=True)
class Args:
    parquet: Path
    out: Path
    log: Path
    name_overrides: Path


def main() -> None:
    args = _parse_args()
    install_logger(args.log)

    if not args.parquet.exists():
        sys.exit(
            f"{args.parquet} not found. Run the scraper first:\n    uv run python -m src.scrape\n"
        )

    df = pl.read_parquet(args.parquet).filter(pl.col("player") != _LEFT_LEAGUE)
    df = apply_name_overrides(df, load_name_overrides(args.name_overrides))
    df = _with_round_zscores(df).with_columns(pl.col("z_in_round").round(_Z_DP))
    df = (
        df.sort("round_time", descending=True)
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
    p.add_argument(
        "--name-overrides",
        type=Path,
        default=_DEFAULT_NAME_OVERRIDES,
        help="JSON {raw_name: display_name} map applied to players/voters; "
        "ignored if the file is missing",
    )
    ns = p.parse_args()
    return Args(parquet=ns.parquet, out=ns.out, log=ns.log, name_overrides=ns.name_overrides)


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
 th { background: #f4f4f4; position: sticky; top: 0; cursor: pointer; user-select: none; }
 th:hover { background: #eaeaea; }
 th .arrow { color: #999; font-size: .8em; }
 tr:nth-child(even) td { background: #fafafa; }
 td.num { text-align: right; font-variant-numeric: tabular-nums; }
 td.date { white-space: nowrap; color: #666; }
 .hidden { display: none; }
</style>
</head>
<body>
<h1>Music League songs</h1>
<div class="toolbar">
  <input id="search" type="search" placeholder="Filter by song title or artist…" autofocus>
  <span id="count"></span>
</div>
<table>
  <thead><tr id="head"></tr></thead>
  <tbody id="rows"></tbody>
</table>
<script>
 const SONGS = __SONGS_JSON__;
 const TOTAL = __COUNT__;
 // column key, header label, whether it sorts numerically
 const COLUMNS = [
   ["score", "Score", true],
   ["z_in_round", "z-score", true],
   ["song", "Song", false],
   ["artist", "Artist", false],
   ["player", "Player", false],
   ["league", "League", false],
   ["round", "Round", false],
   ["round_time", "Date", false],
 ];
 const NUMERIC = new Set(COLUMNS.filter(c => c[2]).map(c => c[0]));

 const head = document.getElementById("head");
 const tbody = document.getElementById("rows");
 const search = document.getElementById("search");
 const counter = document.getElementById("count");

 let sortKey = "round_time";
 let sortDir = -1;  // 1 asc, -1 desc

 function escapeHtml(s) {
   return String(s ?? "").replace(/[&<>"]/g, c => (
     {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]
   ));
 }

 // Signed display: prefix a + on non-negative numbers so direction reads at a glance.
 function signed(v) {
   if (v == null) return "";
   return v >= 0 ? "+" + v : String(v);
 }

 function renderHead() {
   head.innerHTML = COLUMNS.map(([key, label]) => {
     const arrow = key === sortKey ? (sortDir === 1 ? " ▲" : " ▼") : "";
     return `<th data-key="${key}">${escapeHtml(label)}<span class="arrow">${arrow}</span></th>`;
   }).join("");
 }

 function cmpKey(a, b, key, dir) {
   let x = a[key], y = b[key];
   if (NUMERIC.has(key)) {
     x = x == null ? -Infinity : x;
     y = y == null ? -Infinity : y;
     return (x - y) * dir;
   }
   return String(x ?? "").localeCompare(String(y ?? "")) * dir;
 }

 function compare(a, b) {
   const primary = cmpKey(a, b, sortKey, sortDir);
   if (primary !== 0 || sortKey === "z_in_round") return primary;
   // Secondary sort is always by z-score, highest first.
   return cmpKey(a, b, "z_in_round", -1);
 }

 function render() {
   const q = search.value.trim().toLowerCase();
   const rows = SONGS
     .filter(r => !q ||
       r.song.toLowerCase().includes(q) ||
       r.artist.toLowerCase().includes(q))
     .sort(compare);
   tbody.innerHTML = rows.map(r =>
     "<tr>" +
     `<td class="num">${escapeHtml(r.score)}</td>` +
     `<td class="num">${escapeHtml(signed(r.z_in_round))}</td>` +
     `<td>${escapeHtml(r.song)}</td>` +
     `<td>${escapeHtml(r.artist)}</td>` +
     `<td>${escapeHtml(r.player)}</td>` +
     `<td>${escapeHtml(r.league)}</td>` +
     `<td>${escapeHtml(r.round)}</td>` +
     `<td class="date">${escapeHtml(r.round_time)}</td>` +
     "</tr>"
   ).join("");
   counter.textContent = q ? `${rows.length} / ${TOTAL} songs` : `${TOTAL} songs`;
   renderHead();
 }

 head.addEventListener("click", e => {
   const th = e.target.closest("th");
   if (!th) return;
   const key = th.dataset.key;
   if (key === sortKey) {
     sortDir = -sortDir;  // toggle direction on re-click
   } else {
     sortKey = key;
     sortDir = NUMERIC.has(key) ? -1 : 1;  // numbers default high→low, text A→Z
   }
   render();
 });

 search.addEventListener("input", render);
 render();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
