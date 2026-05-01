# music-league-scrape

Scrape every league/round/song you've ever played on https://app.musicleague.com/
into a polars-friendly parquet file.

## Requirements

- [uv](https://docs.astral.sh/uv/) — manages the Python env and pinned deps
  (polars, httpx, selectolax, tenacity, pytest) from `pyproject.toml`.
  Install once with `curl -LsSf https://astral.sh/uv/install.sh | sh`.
- A logged-in browser session on https://app.musicleague.com/ (used once to
  export `auth.curl` — see below).

`uv` will create the env (and install Python 3.14 if needed) on first run.

## Output

Two files, one row per (league, round, song):

- `out/music_league.parquet` — full schema below
- `out/music_league.csv` — convenience subset: `round_time, league, round, player, song, artist, score`

Both are sorted by `round_time, player`.


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

## Usage

```bash
uv run --extra dev pytest tests/ -v            # parser tests (offline, against webpages/ fixtures)
uv run python -m src.scrape                    # full scrape, writes out/music_league.parquet
uv run python -m src.scrape --league <league_id>   # restrict to one or more leagues (repeat)
uv run python -m src.scrape --sleep 1.0            # be nicer to the server
uv run python -m src.scrape --debug                # verbose logging + dump every fetched HTML to debug/
uv run python -m src.analyze                   # build out/analysis.{md,html} from out/music_league.parquet
uv run python -m src.songs_page                # build out/songs.html (every song + JS title filter)
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

## Layout

```
src/
  auth.py    parse cURL export → headers + cookies
  client.py  httpx client with retries; raises LoginRequired on session expiry
  parse.py   selectolax-based HTML parsers (landing, league, round)
  log.py     TeeLogger: stdout/stderr → console + scrape.log
  scrape.py  CLI orchestrator
tests/
  test_parse.py   parser tests against webpages/ fixtures
webpages/
  landing.html, league.html, round.html — saved-from-browser fixtures
out/
  music_league.parquet — scraper output (gitignored)
```
