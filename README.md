# music-league-scrape

Scrape every league/round/song you've ever played on https://app.musicleague.com/
into a polars-friendly parquet file.

## Requirements

- [uv](https://docs.astral.sh/uv/) — manages the Python env and deps from
  `pyproject.toml`. Install once with
  `curl -LsSf https://astral.sh/uv/install.sh | sh`.
- A logged-in browser session on https://app.musicleague.com/ (used once to
  export `auth.curl` — see below).

`uv` will create the env (and install Python 3.14 if needed) on first run.

## Output

Five files in `out/`:

| file                         | produced by                  | what it is                                                        |
| ---------------------------- | ---------------------------- | ----------------------------------------------------------------- |
| `out/music_league.parquet`   | `python -m src.scrape`       | one row per (league, round, song); full schema below              |
| `out/music_league.csv`       | `python -m src.scrape`       | subset: `round_time, league, round, player, song, artist, score`  |
| `out/analysis.md`            | `python -m src.analyze`      | markdown analysis report                                          |
| `out/analysis.html`          | `python -m src.analyze`      | self-contained HTML render of the same                            |
| `out/songs.html`             | `python -m src.songs_page`   | every song embedded inline + JS title-search box                  |

Parquet/CSV are sorted by `round_time, player`. `songs.html` is sorted
newest first.


| column            | type                                       |
| ----------------- | ------------------------------------------ |
| round_time        | datetime[μs, UTC] (round completion time)  |
| league            | str                                        |
| league_id         | str (32-hex)                               |
| round             | str                                        |
| round_id          | str (32-hex)                               |
| player            | str  (submitter display name)              |
| submitter_user_id | str  (32-hex)                              |
| song              | str                                        |
| artist            | str                                        |
| spotify_track_id  | str                                        |
| score             | i64  (the displayed score)                 |
| votes             | list[struct{voter: str \| null, votes: i64}] |

`votes` includes a row with `voter = null` whenever the displayed score exceeds
the sum of explicit voter rows — this is the **forfeit bucket** (Music League
discards votes from players who missed the voting deadline). With the bucket
present, `sum(votes.votes) == score` always holds.

### Anonymisation

Names that look like real first+last (a space, no brackets) are collapsed to
`FirstName LastInitial` at write time. When two players share a first name, the
last-name prefix is extended until each short form is unique
(`Jane Doe` / `Jane Dean` → `Jane Do` / `Jane De`). Single-word handles and
bracketed placeholders (e.g. `[Left the league]`) are left alone. The transform
is idempotent — re-running on already-anonymised data is a no-op.
Implementation: `src/names.py::anonymise_dataframe`, applied inside
`src/scrape.py` before parquet/CSV are written.

## Usage

```bash
uv run --extra dev pytest tests/ -v        # offline tests against webpages/ fixtures
uv run python -m src.scrape                # full scrape (default 0.5s sleep between requests)
uv run python -m src.scrape --league <id>  # restrict to one or more leagues (repeatable)
uv run python -m src.scrape --debug        # verbose logs + dump every fetched HTML to debug/
uv run python -m src.analyze               # build out/analysis.{md,html}
uv run python -m src.songs_page            # build out/songs.html
```

Requires `./auth.curl` in the repo root (gitignored). See below.

## Getting `auth.curl`

The site is auth-gated (Spotify OAuth → session cookie). The scraper does not
log in itself — instead it replays a request that your browser already made
while you were logged in.

### Steps

1. **Log in** to https://app.musicleague.com/ in your normal browser.
2. **Open DevTools** (F12 or ⌘⌥I) and go to the **Network** tab.
3. **Reload the page** (Cmd-R / Ctrl-R) so DevTools captures the request.
4. In the network list, find the **first row** — the document request, usually
   named `/` or `app.musicleague.com`. Its Type column says `document`.
5. **Right-click** that row → **Copy** → **Copy as cURL (bash)**.
   - Chrome/Edge: `Copy → Copy as cURL (bash)`
   - Firefox: `Copy Value → Copy as cURL` (use the bash variant if asked)
   - Safari: `Copy as cURL`
6. **Paste** into a new file `./auth.curl` at the repo root and save.

That's it — the parser reads the `Cookie:` header and the request headers
straight out of that file. There is no need to edit anything; passwords and
2FA are not involved.

### Re-export when the session expires

If a scrape run exits with `LoginRequired: Session expired (302 -> /login/)`,
your session cookie has expired. Re-do steps 1-6 to overwrite `auth.curl` and
re-run. (Cookies typically last days to weeks; just refresh when needed.)

### What's in the file

A single line that looks roughly like:

```bash
curl 'https://app.musicleague.com/' \
  -H 'User-Agent: Mozilla/5.0 ...' \
  -H 'Accept: text/html,...' \
  -H 'Cookie: sessionid=...; csrftoken=...; ...' \
  ...
```

The scraper extracts the `Cookie:` and other headers; everything else is
ignored. **Treat `auth.curl` like a password** — it's a session cookie that
grants access to your Music League account. It's already in `.gitignore`.

