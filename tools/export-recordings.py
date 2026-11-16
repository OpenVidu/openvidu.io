#!/usr/bin/env python3
"""Export the terminal recordings of the `ov` end-to-end tests into docs/assets/recordings/.

    tools/export-recordings.py <recordings-web-dir> [--out docs/assets/recordings] [--dry-run]

The recordings web is the output of ov-cloud-tester (openvidu-deployment,
tests/ov-cloud-tester): one directory per cell, named <cloud>-<variant>-<mode>, holding

    <cell>.cast   the raw recording, in real time (asciicast v2)
    rec.js        window.OVCT_REC = {cast, gaps, ...}, where `cast` is the edited copy: the
                  same run with its long waits cut, and `gaps` says where and how long

For each of the 40 cloud cells (aws, azure, gcp, oracle, digitalocean x ce, pro, elastic, ha
x auto, assisted) it writes

    <cell>.edited.cast   the edited copy. Its header also carries `x_openvidu`: the duration of
                         the raw recording and the cut waits, which the player announces
    <cell>.raw.cast      the raw recording, as it is

and removes any other .cast file from the output directory. If rec.js ever carries the raw
recording too (a `raw` string), it is used when <cell>.cast is missing.

Nothing is written unless every cast of every cell is a valid asciicast v2 and none of them
shows something that names an account, a person or a machine: an unmasked cloud account or
project, a key, a token, a local home directory, this machine's user or host name. The tester
masks those as *** before it writes the web; this is the check after it. A hit names the cell,
the rule and the line, and stops the export (exit 1).

Only the standard library: run it with any Python 3.9+.
"""

from __future__ import annotations

import argparse
import contextlib
import getpass
import json
import re
import socket
import sys
from pathlib import Path

CLOUDS = ("aws", "azure", "gcp", "oracle", "digitalocean")
VARIANTS = ("ce", "pro", "elastic", "ha")
MODES = ("auto", "assisted")
CELLS = [f"{c}-{v}-{m}" for c in CLOUDS for v in VARIANTS for m in MODES]

#: A cut wait shorter than this is not announced (a 3 s wait cut to 2 says nothing).
MIN_GAP_SECONDS = 10

#: The home directories of the cloud images' default users, which a recording may show on a
#: machine of the stack; any other /home/<name> is someone's own machine.
CLOUD_USERS = {"ubuntu", "opc", "azureuser", "admin", "ec2-user", "debian", "root"}

NOT_MASKED = r"(?!\*\*\*)"

#: (rule, pattern) pairs searched in each event's text. Each names what it found, never the
#: value itself: the report must not repeat a leak.
LEAKS = [
    ("a private key (PEM)", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("an AWS access key id", re.compile(r"(?<![A-Za-z0-9])(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("an AWS ARN with its account", re.compile(r"arn:aws[a-z-]*:[a-z0-9-]*:[a-z0-9-]*:\d{12}:")),
    ("a 12-digit number (an AWS account id?)", re.compile(r"(?<![\d.:])\d{12}(?![\d.])")),
    (
        "an Oracle account OCID",
        re.compile(
            r"ocid1\.(?:tenancy|compartment|user|group|vault|key)\.[a-z0-9-]*\.[a-z0-9-]*\."
        ),
    ),
    ("an Azure subscription", re.compile(r"/subscriptions/" + NOT_MASKED + r"[0-9a-fA-F-]{8,}")),
    ("a GCP project", re.compile(r"\bprojects/" + NOT_MASKED + r"[a-z][a-z0-9-]{4,28}[a-z0-9]\b")),
    (
        "a GCP service account",
        re.compile(r"@" + NOT_MASKED + r"[a-z][a-z0-9-]{4,28}[a-z0-9]\.iam\.gserviceaccount\.com"),
    ),
    ("a DigitalOcean token", re.compile(r"\bdo[opr]_v1_[a-f0-9]{20,}")),
    ("a GitHub token", re.compile(r"\bgh[opsur]_[A-Za-z0-9]{20,}")),
    (
        "a JSON Web Token",
        re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]+"),
    ),
    (
        "a kubeconfig credential",
        re.compile(
            r"\b(?:client-key-data|client-certificate-data|token):\s*" + NOT_MASKED + r"\S{16,}"
        ),
    ),
    (
        "a PRO license",
        re.compile(r"--openvidu-pro-license[ =]+" + NOT_MASKED + r"(?![\"']?\$|<)\S{6,}"),
    ),
    ("a macOS home directory", re.compile(r"/Users/[A-Za-z0-9_.-]+")),
]

HOME = re.compile(r"/home/([A-Za-z0-9_.-]+)")
GUID = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
)


class CastError(Exception):
    pass


def parse_cast(text: str, what: str) -> tuple[dict, list[list]]:
    """The header and the events of an asciicast v2 text, or CastError."""
    lines = text.split("\n")
    try:
        header = json.loads(lines[0])
    except (ValueError, IndexError) as e:
        raise CastError(f"{what}: the first line is not a JSON header ({e})") from e
    if not isinstance(header, dict) or header.get("version") != 2:
        raise CastError(f"{what}: not an asciicast v2 header")
    if not isinstance(header.get("width"), int) or not isinstance(header.get("height"), int):
        raise CastError(f"{what}: the header has no width and height")
    events = []
    for n, line in enumerate(lines[1:], start=2):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except ValueError as e:
            raise CastError(f"{what}:{n}: not a JSON event ({e})") from e
        if (
            not isinstance(event, list)
            or len(event) < 3
            or not isinstance(event[0], (int, float))
            or not isinstance(event[2], str)
        ):
            raise CastError(f"{what}:{n}: not an event [time, code, data]")
        events.append(event)
    if not events:
        raise CastError(f"{what}: no events")
    return header, events


def read_rec_js(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise CastError(f"{path}: no window.OVCT_REC object")
    try:
        data = json.loads(text[start : end + 1])
    except ValueError as e:
        raise CastError(f"{path}: the OVCT_REC object is not JSON ({e})") from e
    if not isinstance(data.get("cast"), str):
        raise CastError(f"{path}: OVCT_REC has no `cast` (the edited recording)")
    return data


def gap_seconds(gap: dict) -> float:
    """How long a cut wait was: its own number if the tester gives one, else read from its
    label ("⏩ 8 min", "⏩ 16 s", "⏩ 1 h 5 min")."""
    for key in ("realSec", "seconds", "secs"):
        if isinstance(gap.get(key), (int, float)):
            return float(gap[key])
    total = 0.0
    for number, unit in re.findall(r"(\d+(?:\.\d+)?)\s*(h|min|s)\b", str(gap.get("label", ""))):
        total += float(number) * {"h": 3600, "min": 60, "s": 1}[unit]
    return total


def leaks_in(events: list[list], cell: str, what: str, me: set[str]) -> list[str]:
    """Every leak shape found in the events' text, as report lines (no values)."""
    found = []
    for i, event in enumerate(events):
        if event[1] not in ("o", "m", "i"):
            continue
        text = event[2]
        hits = [rule for rule, pattern in LEAKS if pattern.search(text)]
        for m in HOME.finditer(text):
            if m.group(1) not in CLOUD_USERS:
                hits.append("a home directory of a person's machine (/home/<name>)")
        if cell.startswith("azure-") and GUID.search(text):
            # Azure prints its subscription and tenant as GUIDs; nothing of the stack is one.
            hits.append("a GUID in an Azure recording (a subscription or tenant id?)")
        lowered = text.lower()
        hits += ["this machine's user or host name" for value in me if value in lowered]
        for rule in dict.fromkeys(hits):
            found.append(f"{cell} ({what}), event {i + 1} at {event[0]}s: {rule}")
    return found


def this_machine() -> set[str]:
    """This machine's user and host names, lower-cased: a recording must never show them."""
    names = set()
    with contextlib.suppress(Exception):
        names.add(getpass.getuser())
    names.add(socket.gethostname().split(".")[0])
    return {n.lower() for n in names if len(n) >= 4}


def to_text(header: dict, events: list[list]) -> str:
    out = [json.dumps(header, ensure_ascii=False, separators=(",", ":"))]
    out += [json.dumps(e, ensure_ascii=False, separators=(",", ":")) for e in events]
    return "\n".join(out) + "\n"


def export(web: Path, out: Path, dry_run: bool) -> int:
    me = this_machine()
    problems: list[str] = []
    outputs: dict[str, str] = {}
    summary = []
    for cell in CELLS:
        cell_dir = web / cell
        if not cell_dir.is_dir():
            problems.append(f"{cell}: no directory {cell_dir}")
            continue
        try:
            rec = read_rec_js(cell_dir / "rec.js")
            raw_file = cell_dir / f"{cell}.cast"
            if raw_file.is_file():
                raw_text = raw_file.read_text(encoding="utf-8")
            elif isinstance(rec.get("raw"), str):
                raw_text = rec["raw"]
            else:
                raise CastError(f"{cell}: no raw recording ({raw_file.name}, or `raw` in rec.js)")
            edited_header, edited_events = parse_cast(rec["cast"], f"{cell} edited")
            _, raw_events = parse_cast(raw_text, f"{cell} raw")
        except (OSError, CastError) as e:
            problems.append(str(e))
            continue

        problems += leaks_in(edited_events, cell, "edited", me)
        problems += leaks_in(raw_events, cell, "raw", me)
        if not any(e[1] == "m" and str(e[2]).startswith("Deploy") for e in edited_events):
            print(f"warning: {cell}: no «Deploy» step marker", file=sys.stderr)

        raw_duration = round(float(raw_events[-1][0]), 1)
        gaps = [
            {"at": round(float(g["at"]), 3), "label": str(g.get("label", "")).strip()}
            for g in rec.get("gaps") or []
            if isinstance(g, dict)
            and isinstance(g.get("at"), (int, float))
            and gap_seconds(g) >= MIN_GAP_SECONDS
        ]
        edited_header = {
            **edited_header,
            "x_openvidu": {"raw_duration": raw_duration, "gaps": gaps},
        }
        outputs[f"{cell}.edited.cast"] = to_text(edited_header, edited_events)
        outputs[f"{cell}.raw.cast"] = raw_text if raw_text.endswith("\n") else raw_text + "\n"
        summary.append((cell, float(edited_events[-1][0]), raw_duration))

    if problems:
        print("Nothing was exported:", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1

    total = 0
    for cell, edited, raw in summary:
        e_size = len(outputs[f"{cell}.edited.cast"].encode())
        r_size = len(outputs[f"{cell}.raw.cast"].encode())
        total += e_size + r_size
        print(
            f"{cell:30s} edited {edited:6.0f} s {e_size / 1024:7.1f} KiB"
            f"   raw {raw:6.0f} s {r_size / 1024:7.1f} KiB"
        )
    print(f"{len(summary)} cells, {len(outputs)} files, {total / 1024 / 1024:.2f} MiB")
    if dry_run:
        print("--dry-run: nothing written")
        return 0

    out.mkdir(parents=True, exist_ok=True)
    for stale in sorted(out.glob("*.cast")):
        if stale.name not in outputs:
            stale.unlink()
            print(f"removed {stale}")
    for name, text in outputs.items():
        path = out / name
        if not path.is_file() or path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
    print(f"wrote {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    repo = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Export the ov e2e terminal recordings into the site's assets."
    )
    parser.add_argument("web", type=Path, help="the recordings web directory (one dir per cell)")
    parser.add_argument(
        "--out",
        type=Path,
        default=repo / "docs" / "assets" / "recordings",
        help="output directory (default: docs/assets/recordings of this repository)",
    )
    parser.add_argument("--dry-run", action="store_true", help="check and report, write nothing")
    args = parser.parse_args(argv)
    if not args.web.is_dir():
        parser.error(f"{args.web} is not a directory")
    return export(args.web, args.out, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
