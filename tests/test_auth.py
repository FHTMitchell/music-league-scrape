"""Tests for the cURL parser."""

from __future__ import annotations

from pathlib import Path

from src.auth import parse_curl_file

_SAMPLE_CURL = r"""curl 'https://app.musicleague.com/' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh)' \
  -H 'Accept: text/html' \
  -H 'Cookie: sessionid=abc123; csrftoken=xyz789; remember=true' \
  -H 'Host: app.musicleague.com' \
  -H ':authority: app.musicleague.com' \
  -b 'extra=cookie-from-b'
"""


def test_parse_curl_file_extracts_cookies_and_headers(tmp_path: Path) -> None:
    f = tmp_path / "auth.curl"
    f.write_text(_SAMPLE_CURL)
    auth = parse_curl_file(f)

    assert auth.cookies == {
        "sessionid": "abc123",
        "csrftoken": "xyz789",
        "remember": "true",
        "extra": "cookie-from-b",
    }
    assert auth.headers["User-Agent"] == "Mozilla/5.0 (Macintosh)"
    assert auth.headers["Accept"] == "text/html"


def test_parse_curl_drops_pseudo_and_host_headers(tmp_path: Path) -> None:
    f = tmp_path / "auth.curl"
    f.write_text(_SAMPLE_CURL)
    auth = parse_curl_file(f)

    assert "Host" not in auth.headers
    assert ":authority" not in auth.headers
    assert "Cookie" not in auth.headers and "cookie" not in auth.headers


def test_parse_curl_accepts_line_continuations(tmp_path: Path) -> None:
    f = tmp_path / "auth.curl"
    f.write_text("curl 'x' \\\n  -H 'Cookie: a=1; b=2'\n")
    auth = parse_curl_file(f)
    assert auth.cookies == {"a": "1", "b": "2"}
