"""Console output and the machine-readable step journal.

Kept dependency-free (no rich): the publish runs in GitHub Actions logs most of the time,
where plain prefixed lines read better than boxes.
"""

from __future__ import annotations

import json
import shlex
import sys
from collections.abc import Sequence
from pathlib import Path


class Reporter:
    def __init__(self, *, verbosity: int = 0, as_json: bool = False, color: bool = True) -> None:
        self.verbosity = verbosity
        self.as_json = as_json
        self.color = color and sys.stdout.isatty()

    # -- styling ------------------------------------------------------------------------

    def _paint(self, text: str, code: str) -> str:
        return f"\033[{code}m{text}\033[0m" if self.color else text

    def _emit(self, line: str) -> None:
        if not self.as_json:
            print(line, flush=True)

    # -- messages -----------------------------------------------------------------------

    def heading(self, text: str) -> None:
        self._emit("")
        self._emit(self._paint(text, "1"))

    def step(self, name: str, text: str) -> None:
        self._emit(f"  {self._paint('▸', '36')} {text}")
        if self.as_json:
            self.event("step", name=name, title=text)

    def info(self, text: str) -> None:
        self._emit(f"    {text}")

    def detail(self, text: str) -> None:
        if self.verbosity >= 1:
            self._emit(f"    {self._paint(text, '2')}")

    def warn(self, text: str) -> None:
        self._emit(f"  {self._paint('warning:', '33')} {text}")
        if self.as_json:
            self.event("warning", message=text)

    def error(self, text: str) -> None:
        print(f"{self._paint('error:', '31')} {text}", file=sys.stderr, flush=True)

    def success(self, text: str) -> None:
        self._emit("")
        self._emit(self._paint(text, "32"))

    def command(
        self, argv: Sequence[str], *, cwd: Path | None = None, skipped: bool = False
    ) -> None:
        if self.verbosity < 2 and not skipped:
            return
        rendered = " ".join(shlex.quote(part) for part in argv)
        prefix = "would run" if skipped else "run"
        location = f" (in {cwd})" if cwd is not None and self.verbosity >= 2 else ""
        self._emit(f"    {self._paint(prefix, '2')} {rendered}{location}")

    def result(self, name: str, **fields: object) -> None:
        """Report the outcome of a step: printed when verbose, always in the JSON journal."""
        if self.as_json:
            self.event("result", name=name, **fields)
            return
        if self.verbosity >= 1 and fields:
            rendered = ", ".join(f"{key}={value}" for key, value in fields.items())
            self._emit(f"    {self._paint(rendered, '2')}")

    def event(self, kind: str, **fields: object) -> None:
        if self.as_json:
            print(json.dumps({"event": kind, **fields}, default=str), flush=True)
