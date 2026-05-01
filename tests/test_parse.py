"""Parser tests against saved fixtures in ``webpages/``."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from src.parse import parse_landing, parse_league, parse_round

_FIXTURES = Path(__file__).resolve().parent.parent / "webpages"
_BASIC_LEAGUE_ID = "417481c3557c40779d6aa0bcc6e805fb"
_JAMIES_ROUND_ID = "21ce32d19b2645248b84592a99b46655"


def test_parse_landing_extracts_completed_leagues() -> None:
    tiles = parse_landing((_FIXTURES / "landing.html").read_text())
    assert len(tiles) == 5
    basic = next(t for t in tiles if t.name == "Basic League")
    assert basic.league_id == _BASIC_LEAGUE_ID
    assert basic.status == "COMPLETE"


def test_parse_league_returns_name_and_rounds() -> None:
    league = parse_league((_FIXTURES / "league.html").read_text())
    assert league.name == "Basic League"
    assert len(league.rounds) == 8
    assert all(r.status == "COMPLETE" for r in league.rounds)
    jamie = next(r for r in league.rounds if r.round_id == _JAMIES_ROUND_ID)
    assert jamie.time == datetime(2026, 4, 14, 21, 48, 15, tzinfo=UTC)


def test_parse_round_song_fields_and_votes() -> None:
    html = (_FIXTURES / "round.html").read_text()
    rnd = parse_round(
        html, league="Basic League", league_id=_BASIC_LEAGUE_ID, round_id=_JAMIES_ROUND_ID
    )
    assert rnd.name == "Jamie\u2019s round"
    nightswimming = next(s for s in rnd.songs if s.song == "Nightswimming")
    assert nightswimming.artist == "R.E.M."
    assert nightswimming.player == "Sam Mitchell"
    assert nightswimming.score == 6
    assert nightswimming.spotify_track_id == "6G0NzOx2jEPFsSmhr9N8Ys"

    by_voter = {v.voter: v.votes for v in nightswimming.votes}
    assert by_voter["Fred Norman"] == 2
    assert by_voter["harryg"] == -1
    assert sum(by_voter.values()) == nightswimming.score
    assert None not in by_voter  # explicit votes already total to score


def test_parse_round_forfeit_bucket_is_added_when_score_exceeds_explicit_votes() -> None:
    """Synthetic page: score header says 5 but explicit voters sum to 3 → None bucket of 2."""
    html = """
    <div class="card mb-4" id="spotify:track:fakeid">
      <div class="card-body">
        <a href="/user/00000000000000000000000000000000/" title="Album art"></a>
        <div class="col text-truncate">
          <h6 class="card-title"><a target="_blank">Fake Song</a></h6>
          <p class="card-text">Fake Artist</p>
        </div>
        <div class="col-auto text-end"><h3 class="m-0">5</h3></div>
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
    rnd = parse_round(html, league="L", league_id="x" * 32, round_id="y" * 32)
    assert len(rnd.songs) == 1
    by_voter = {v.voter: v.votes for v in rnd.songs[0].votes}
    assert by_voter == {"Voter A": 3, None: 2}
