"""Parse a `Copy as cURL (bash)` export into headers + cookies."""

from __future__ import annotations

import logging
import shlex
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

_HEADER_FLAGS = frozenset({"-H", "--header"})
_COOKIE_FLAGS = frozenset({"-b", "--cookie"})
_DROP_HEADERS = frozenset({"host", "content-length"})


@dataclass(frozen=True)
class CurlAuth:
    headers: dict[str, str] = field(default_factory=dict)
    cookies: dict[str, str] = field(default_factory=dict)


def parse_curl_file(path: Path) -> CurlAuth:
    """Read a cURL command exported from browser DevTools.

    Strips ``Host`` / ``Content-Length`` and pseudo (``:authority``) headers
    so the result is safe to hand straight to ``httpx.Client``.
    """
    raw = path.read_text().replace("\\\n", " ").replace("\\\r\n", " ")
    tokens = iter(shlex.split(raw))

    headers: dict[str, str] = {}
    cookies: dict[str, str] = {}

    for tok in tokens:
        if tok in _HEADER_FLAGS:
            _consume_header(next(tokens, None), headers)
        elif tok in _COOKIE_FLAGS:
            cookies.update(_parse_cookie_string(next(tokens, None) or ""))

    cookie_header = headers.pop("Cookie", None) or headers.pop("cookie", None)
    if cookie_header:
        cookies.update(_parse_cookie_string(cookie_header))

    headers = {k: v for k, v in headers.items() if not _is_drop_header(k)}
    logger.info("parsed auth: %d headers, %d cookies", len(headers), len(cookies))
    return CurlAuth(headers=headers, cookies=cookies)


def _consume_header(value: str | None, headers: dict[str, str]) -> None:
    if not value or ":" not in value:
        return
    name, _, val = value.partition(":")
    headers[name.strip()] = val.strip()


def _parse_cookie_string(s: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in s.split(";"):
        part = part.strip()
        if "=" not in part:
            continue
        k, _, v = part.partition("=")
        out[k.strip()] = v.strip()
    return out


def _is_drop_header(name: str) -> bool:
    return name.startswith(":") or name.lower() in _DROP_HEADERS
