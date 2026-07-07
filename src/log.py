"""TeeLogger: duplicate stdout/stderr to a log file."""

from __future__ import annotations

import logging
import sys
import time
from pathlib import Path
from typing import IO

logger = logging.getLogger(__name__)

# Fixed 5-char labels (padded/abbreviated) keyed by level, so every line aligns.
_LEVEL_LABELS = {
    logging.DEBUG: "DEBUG",
    logging.INFO: "INFO ",
    logging.WARNING: "WARN ",
    logging.ERROR: "ERROR",
    logging.CRITICAL: "CRIT ",
}
_LEVEL_COLORS = {
    logging.DEBUG: "\033[90m",  # grey
    logging.INFO: "\033[32m",  # green
    logging.WARNING: "\033[33m",  # yellow
    logging.ERROR: "\033[31m",  # red
    logging.CRITICAL: "\033[1;31m",  # bold red
}
_RESET = "\033[0m"


class ElapsedFormatter(logging.Formatter):
    """Prefix each record with seconds elapsed since app startup (e.g. ``5.3s``).

    The level name is rendered as a fixed 5-char label. When ``color`` is set,
    that label is wrapped in an ANSI severity color (grey/green/yellow/red).
    """

    def __init__(self, fmt: str, *, start: float, color: bool) -> None:
        super().__init__(fmt)
        self._start = start
        self._color = color

    def format(self, record: logging.LogRecord) -> str:
        record.elapsed = f"{record.created - self._start:.1f}s"
        label = _LEVEL_LABELS.get(record.levelno, record.levelname[:5].ljust(5))
        label = f"[{label}]"
        if self._color:
            label = f"{_LEVEL_COLORS.get(record.levelno, '')}{label}{_RESET}"
        record.levellabel = label
        return super().format(record)


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
    """Tee ``stdout``/``stderr`` to ``log_path`` (truncated on each run).

    Also configures the ``logging`` root with the same destination so library
    logs land in the same file. ``debug=True`` lowers the level to DEBUG and
    quiets ``httpx`` to INFO so it does not drown the signal.
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handle = open(log_path, "w", buffering=1)
    # Tee plain stdout/stderr (from ``print``) into the log file.
    sys.stdout = TeeStream(sys.__stdout__, handle)  # type: ignore[assignment]
    sys.stderr = TeeStream(sys.__stderr__, handle)  # type: ignore[assignment]

    start = time.time()
    fmt = "%(elapsed)s %(levellabel)s %(name)s: %(message)s"
    is_tty = bool(getattr(sys.__stderr__, "isatty", lambda: False)())

    # Two handlers so color only ever reaches the terminal, never the file.
    term_handler = logging.StreamHandler(sys.__stderr__)
    term_handler.setFormatter(ElapsedFormatter(fmt, start=start, color=is_tty))
    file_handler = logging.StreamHandler(handle)
    file_handler.setFormatter(ElapsedFormatter(fmt, start=start, color=False))

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.DEBUG if debug else logging.INFO)
    root.addHandler(term_handler)
    root.addHandler(file_handler)
    if debug:
        logging.getLogger("httpx").setLevel(logging.INFO)
        logging.getLogger("httpcore").setLevel(logging.INFO)
