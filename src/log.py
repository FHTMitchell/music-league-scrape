"""TeeLogger: duplicate stdout/stderr to a log file."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import IO

logger = logging.getLogger(__name__)


class TeeStream:
    def __init__(self, *streams: IO[str]) -> None:
        self._streams = streams

    def write(self, s: str) -> int:
        for stream in self._streams:
            stream.write(s)
            stream.flush()
        return len(s)

    def flush(self) -> None:
        for stream in self._streams:
            stream.flush()


def install(log_path: Path, *, debug: bool = False) -> None:
    """Tee ``stdout``/``stderr`` to ``log_path`` (appended).

    Also configures the ``logging`` root with the same destination so library
    logs land in the same file. ``debug=True`` lowers the level to DEBUG and
    quiets ``httpx`` to INFO so it does not drown the signal.
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handle = open(log_path, "a", buffering=1)
    sys.stdout = TeeStream(sys.__stdout__, handle)  # type: ignore[assignment]
    sys.stderr = TeeStream(sys.__stderr__, handle)  # type: ignore[assignment]
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
        force=True,
    )
    if debug:
        logging.getLogger("httpx").setLevel(logging.INFO)
        logging.getLogger("httpcore").setLevel(logging.INFO)
