"""The finding model shared by every lint check."""

from __future__ import annotations

from dataclasses import dataclass

ERROR = "error"
WARN = "warn"
INFO = "info"

SEVERITY_ORDER = {ERROR: 0, WARN: 1, INFO: 2}


@dataclass(frozen=True)
class Finding:
    check: str
    severity: str
    file: str
    line: int
    message: str
    hint: str = ""
