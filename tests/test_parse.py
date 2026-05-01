"""Parser tests against anonymised fixtures in ``webpages/``.

The fixtures are scrubbed real pages (see ``src/anonymise_fixtures.py``); their
fake player/voter names are recorded in ``tests/fixture_names.json`` so these
tests assert name handling without hardcoding any specific name.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from src.parse import parse_landing, parse_league, parse_round

_FIXTURES = Path(__file__).resolve().parent.parent / "webpages"
_MANIFEST = json.loads((Path(__file__).resolve().parent / "fixture_names.json").read_text())
_BASIC_LEAGUE_ID = "417481c3557c40779d6aa0bcc6e805fb"
_JAMIES_ROUND_ID = "21ce32d19b2645248b84592a99b46655"
_FORFEIT_ROUND_ID = "9e14f8f4a39549d2bf077f04884d0cd9"


def test_parse_landing_extracts_completed_leagues() -> None:
    tiles = parse_landing((_FIXTURES / "landing.html").read_text())
    assert len(tiles) == 6
    basic = next(t for t in tiles if t.name == "Basic League")
    assert basic.league_id == _BASIC_LEAGUE_ID
    assert basic.status == "COMPLETE"


def test_parse_league_returns_rounds_and_timestamps() -> None:
    league = parse_league((_FIXTURES / "league.html").read_text())
    assert len(league.rounds) == 8
    assert all(r.status == "COMPLETE" for r in league.rounds)
    jamie = next(r for r in league.rounds if r.round_id == _JAMIES_ROUND_ID)
    assert jamie.time == datetime(2026, 4, 14, 21, 48, 15, tzinfo=UTC)


def test_parse_round_song_fields_and_votes() -> None:
    html = (_FIXTURES / "round.html").read_text()
    rnd = parse_round(
        html,
        league="Basic League",
        league_id=_BASIC_LEAGUE_ID,
        round_id=_JAMIES_ROUND_ID,
        round_name="Jamie’s round",
    )
    assert rnd.name == "Jamie’s round"

    nightswimming = next(s for s in rnd.songs if s.song == "Nightswimming")
    assert nightswimming.artist == "R.E.M."
    assert nightswimming.spotify_track_id == "6G0NzOx2jEPFsSmhr9N8Ys"
    assert nightswimming.score == 6
    assert nightswimming.received == 6
    assert nightswimming.forfeited is False

    # Every submitter/voter name is one of the fixture's fake names.
    known = set(_MANIFEST["round.html"]["names"])
    assert nightswimming.player in known
    assert {v.voter for v in nightswimming.votes} <= known
    # Explicit votes total to the displayed score (no forfeit on this song).
    assert sum(v.votes for v in nightswimming.votes) == nightswimming.score


def test_parse_round_forfeit_fixture_splits_score_from_received() -> None:
    """The anonymised forfeit round has struck-through (forfeited) songs."""
    rnd = parse_round(
        (_FIXTURES / "round_forfeit.html").read_text(),
        league="Basic League",
        league_id=_BASIC_LEAGUE_ID,
        round_id=_FORFEIT_ROUND_ID,
    )
    forfeited = [s for s in rnd.songs if s.forfeited]
    assert forfeited, "fixture should contain at least one forfeited song"
    for song in forfeited:
        # Song earned its votes; the submitter banked 0 (or negative).
        assert song.score == sum(v.votes for v in song.votes)
        assert song.received <= 0
        assert song.received != song.score


def _forfeit_card(struck_score: str, banked: str) -> str:
    """A song card whose score is struck through (submitter forfeit)."""
    return f"""
    <div class="card mb-4" id="spotify:track:fakeid">
      <div class="card-body">
        <a href="/user/00000000000000000000000000000000/" title="Album art"></a>
        <div class="col text-truncate">
          <h6 class="card-title"><a target="_blank">Fake Song</a></h6>
          <p class="card-text">Fake Artist</p>
        </div>
        <div class="col-auto text-end">
          <h3 class="m-0"><s class="text-danger">{struck_score}</s> {banked}</h3>
        </div>
        <div class="card mt-3 rank-1"><h6 class="text-body fw-semibold">Submitter</h6></div>
      </div>
      <div class="card-footer" id="votes-fakeid">
        <div class="row align-items-start">
          <b class="d-block text-truncate text-body">Voter A</b>
          <h6 class="m-0">3</h6>
        </div>
      </div>
    </div>
    """


def test_parse_round_forfeit_splits_earned_score_from_banked_points() -> None:
    """Struck-through score: the song earned 5, the submitter banked 0."""
    rnd = parse_round(_forfeit_card("5", "0"), league="L", league_id="x" * 32, round_id="y" * 32)
    assert len(rnd.songs) == 1
    song = rnd.songs[0]
    assert song.score == 5  # earned from voters
    assert song.received == 0  # banked after forfeit
    assert song.forfeited is True
    assert {v.voter: v.votes for v in song.votes} == {"Voter A": 3}


def test_parse_round_forfeit_keeps_negative_banked_from_downvotes() -> None:
    """In a downvote league a forfeiting submitter still eats the downvotes."""
    rnd = parse_round(_forfeit_card("3", "-1"), league="L", league_id="x" * 32, round_id="y" * 32)
    song = rnd.songs[0]
    assert song.score == 3
    assert song.received == -1
    assert song.forfeited is True
