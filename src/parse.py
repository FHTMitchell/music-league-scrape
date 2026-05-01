"""Pure HTML parsers for Music League pages.

No I/O, no globals: each function takes raw HTML and returns dataclasses.
Selectors verified against fixtures in ``webpages/``.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime

from selectolax.parser import HTMLParser, Node

logger = logging.getLogger(__name__)

_HEX32 = re.compile(r"^[0-9a-f]{32}$")
_LEAGUE_HREF = re.compile(r"/l/([0-9a-f]{32})/?$")
_USER_HREF = re.compile(r"/user/([0-9a-f]{32})/?")
_X_DATA_STATUS = re.compile(r"status:\s*'([^']+)'")
_DATE_FNS_PARSE = re.compile(r"dateFns\.parse\('([^']+)'\)")


@dataclass(frozen=True)
class LeagueTile:
    league_id: str
    name: str
    status: str  # COMPLETE | IN_PROGRESS | NOT_STARTED


@dataclass(frozen=True)
class RoundEntry:
    round_id: str
    name: str
    status: str
    time: datetime | None  # round completion timestamp (UTC)


@dataclass(frozen=True)
class League:
    name: str
    rounds: list[RoundEntry]


@dataclass(frozen=True)
class Vote:
    voter: str | None  # None marks the forfeit bucket (score - sum(explicit))
    votes: int


@dataclass
class SongRow:
    league: str
    league_id: str
    round: str
    round_id: str
    round_time: datetime | None
    spotify_track_id: str
    song: str
    artist: str
    player: str
    submitter_user_id: str | None
    score: int
    votes: list[Vote] = field(default_factory=list)


@dataclass(frozen=True)
class Round:
    name: str
    songs: list[SongRow]


def parse_landing(html: str) -> list[LeagueTile]:
    """Extract every league tile from the user's home page."""
    tree = HTMLParser(html)
    raw_tiles = tree.css("div.league-tile")
    league_links = tree.css('a[href*="/l/"]')
    logger.debug(
        "landing: %d bytes, %d .league-tile nodes, %d /l/ links",
        len(html),
        len(raw_tiles),
        len(league_links),
    )

    seen: set[str] = set()
    tiles: list[LeagueTile] = []
    for tile in raw_tiles:
        link = tile.css_first("a.stretched-link")
        if link is None:
            logger.debug("league-tile has no a.stretched-link, skipping")
            continue
        match = _LEAGUE_HREF.search((link.attributes.get("href") or "").rstrip("/") + "/")
        if not match or match.group(1) in seen:
            continue
        seen.add(match.group(1))
        tiles.append(
            LeagueTile(
                league_id=match.group(1),
                name=_text(link),
                status=tile.attributes.get("data-league-status") or "",
            )
        )
    return tiles


def parse_league(html: str) -> League:
    """Extract league name and ordered round entries from a league page."""
    tree = HTMLParser(html)
    title = tree.css_first("title")
    name = _text(title)

    seen: set[str] = set()
    rounds: list[RoundEntry] = []
    for item in tree.css("div.league-round-item"):
        rid = item.attributes.get("id") or ""
        if not _HEX32.match(rid) or rid in seen:
            continue
        seen.add(rid)
        x_data = item.attributes.get("x-data") or ""
        status_match = _X_DATA_STATUS.search(x_data)
        title_node = item.css_first("h5.card-title")
        rounds.append(
            RoundEntry(
                round_id=rid,
                name=_text(title_node),
                status=status_match.group(1) if status_match else "",
                time=_extract_round_time(item),
            )
        )
    return League(name=name, rounds=rounds)


def _extract_round_time(item: Node) -> datetime | None:
    """Pull the ISO timestamp out of ``dateFns.parse('...')`` inside a round item.

    Each round item wraps its completion time in an Alpine ``x-data`` attribute
    on a ``<span>`` such as ``{ts: dateFns.parse('2026-04-14T21:48:15Z'), ...}``.
    Returns ``None`` for in-progress rounds where no such span exists.
    """
    for span in item.css("span[x-data]"):
        attr = span.attributes.get("x-data") or ""
        m = _DATE_FNS_PARSE.search(attr)
        if not m:
            continue
        try:
            return datetime.fromisoformat(m.group(1).replace("Z", "+00:00"))
        except ValueError:
            logger.warning("could not parse round timestamp %r", m.group(1))
            return None
    return None


def parse_round(
    html: str,
    *,
    league: str,
    league_id: str,
    round_id: str,
    round_time: datetime | None = None,
    round_name: str | None = None,
) -> Round:
    """Extract one ``SongRow`` per submitted track.

    Works on both the full round page and the ``-/results`` htmx fragment.
    If ``round_name`` is supplied (caller already knows it from the rounds
    list), the header lookup is skipped — necessary for the fragment, where
    the round-header card is not present.

    Adds ``Vote(voter=None, votes=score - sum(explicit))`` whenever the
    displayed score does not equal the sum of explicit voter rows. This
    captures vote-forfeit penalties without hiding them.
    """
    tree = HTMLParser(html)
    if round_name is None:
        header = tree.css_first("div.card div.card-body h5.card-title")
        round_name = _text(header)

    songs: list[SongRow] = [
        _parse_song(
            card,
            league=league,
            league_id=league_id,
            round_=round_name,
            round_id=round_id,
            round_time=round_time,
        )
        for card in tree.css('div.card[id^="spotify:track:"]')
    ]
    return Round(name=round_name, songs=songs)


def _parse_song(
    card: Node,
    *,
    league: str,
    league_id: str,
    round_: str,
    round_id: str,
    round_time: datetime | None,
) -> SongRow:
    track_id = (card.attributes.get("id") or "").removeprefix("spotify:track:")
    title_node = card.css_first("h6.card-title a")
    artist = _first_card_text(card)
    score = _parse_score(card)
    submitter_user_id, player = _parse_submitter(card)
    votes = _parse_votes(card)

    forfeit = score - sum(v.votes for v in votes)
    if forfeit:
        votes.append(Vote(voter=None, votes=forfeit))

    return SongRow(
        league=league,
        league_id=league_id,
        round=round_,
        round_id=round_id,
        round_time=round_time,
        spotify_track_id=track_id,
        song=_text(title_node),
        artist=artist,
        player=player,
        submitter_user_id=submitter_user_id,
        score=score,
        votes=votes,
    )


def _first_card_text(card: Node) -> str:
    """Artist line: the first ``p.card-text`` inside the truncated text column."""
    text_col = card.css_first("div.card-body div.col.text-truncate")
    if text_col is None:
        return ""
    first = text_col.css_first("p.card-text")
    return _text(first)


def _parse_score(card: Node) -> int:
    node = card.css_first("div.col-auto.text-end h3.m-0")
    if node is None:
        return 0
    try:
        return int(_text(node))
    except ValueError:
        logger.warning("non-integer score on card id=%s", card.attributes.get("id"))
        return 0


def _parse_submitter(card: Node) -> tuple[str | None, str]:
    user_id: str | None = None
    art = card.css_first('a[title="Album art"]')
    if art is not None:
        m = _USER_HREF.search(art.attributes.get("href") or "")
        if m:
            user_id = m.group(1)

    rank_card = card.css_first('div.card.mt-3[class*="rank-"]')
    if rank_card is None:
        return user_id, ""
    name_node = rank_card.css_first("h6.text-body.fw-semibold")
    return user_id, _text(name_node)


def _parse_votes(card: Node) -> list[Vote]:
    footer = card.css_first('div.card-footer[id^="votes-"]')
    if footer is None:
        return []
    votes: list[Vote] = []
    for row in footer.css("div.row.align-items-start"):
        name_node = row.css_first("b.d-block.text-truncate.text-body")
        if name_node is None:
            continue
        count_nodes = row.css("h6.m-0")
        if not count_nodes:
            continue
        try:
            n = int(_text(count_nodes[-1]))
        except ValueError:
            continue
        votes.append(Vote(voter=_text(name_node), votes=n))
    return votes


def _text(node: Node | None) -> str:
    if node is None:
        return ""
    return (node.text(deep=True, separator=" ", strip=True) or "").strip()
