"""Authenticated httpx client for app.musicleague.com."""

from __future__ import annotations

import logging
import time

import httpx
from tenacity import (
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.auth import CurlAuth

logger = logging.getLogger(__name__)

BASE_URL = "https://app.musicleague.com"
_RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})


class LoginRequired(RuntimeError):
    """Raised when the session cookie has expired (server redirects to /login/)."""


class _RetryableStatus(Exception):
    pass


class MusicLeagueClient:
    """Thin wrapper over ``httpx.Client`` with retries and rate limiting.

    The server uses 302 → ``/login/`` to signal expired sessions; that case is
    raised as ``LoginRequired`` so the caller can prompt the user to re-export
    ``auth.curl`` instead of silently retrying.
    """

    def __init__(self, auth: CurlAuth, *, sleep_seconds: float = 0.5) -> None:
        self._sleep_seconds = sleep_seconds
        self._client = httpx.Client(
            base_url=BASE_URL,
            headers=auth.headers,
            cookies=auth.cookies,
            timeout=30.0,
            follow_redirects=True,
        )

    def __enter__(self) -> MusicLeagueClient:
        return self

    def __exit__(self, *_: object) -> None:
        self._client.close()

    def get_html(self, path: str) -> str:
        for attempt in Retrying(
            stop=stop_after_attempt(4),
            wait=wait_exponential(multiplier=1, min=1, max=20),
            retry=retry_if_exception_type((httpx.TransportError, _RetryableStatus)),
            reraise=True,
        ):
            with attempt:
                resp = self._client.get(path)
                self._guard_login(resp, path)
                if resp.status_code in _RETRY_STATUSES:
                    raise _RetryableStatus(f"{resp.status_code} {path}")
                resp.raise_for_status()
                logger.debug(
                    "GET %s -> %d, final=%s, %d bytes, %d redirects",
                    path,
                    resp.status_code,
                    resp.url,
                    len(resp.text),
                    len(resp.history),
                )
                time.sleep(self._sleep_seconds)
                return resp.text
        raise RuntimeError("unreachable")

    @staticmethod
    def _guard_login(resp: httpx.Response, path: str) -> None:
        if "/login" in resp.url.path:
            raise LoginRequired(
                f"Session expired (redirected to {resp.url.path}). Re-export auth.curl. path={path}"
            )
        for hop in resp.history:
            if "/login" in (hop.headers.get("location") or ""):
                raise LoginRequired(
                    f"Session expired (redirect chain hit /login). Re-export auth.curl. path={path}"
                )
