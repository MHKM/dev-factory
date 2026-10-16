#!/usr/bin/env python3
"""factory panel inbox monitor (plugin monitor, interactive sessions only).

Tails .factory/inbox.jsonl, which the panel server appends to when the human
acts in the panel, and prints one line per entry. Claude Code delivers each
printed line to the orchestrator as a notification, which wakes it up.
The panel has already applied the decision; the line only tells the
orchestrator what happened so it continues from the state.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

POLL_SECONDS = 1.0


def find_factory() -> Path | None:
    current = Path(os.getcwd()).resolve()
    for d in [current, *current.parents]:
        if (d / ".factory").is_dir():
            return d / ".factory"
    return None


def main() -> None:
    inbox = None
    position = 0
    while True:
        if inbox is None:
            fac = find_factory()
            if fac is not None:
                inbox = fac / "inbox.jsonl"
                # Start at the end: earlier entries belong to previous sessions.
                position = inbox.stat().st_size if inbox.exists() else 0
        elif inbox.exists():
            size = inbox.stat().st_size
            if size < position:
                position = 0
            if size > position:
                with open(inbox, "rb") as f:
                    f.seek(position)
                    chunk = f.read(size - position)
                position = size
                for line in chunk.decode("utf-8", "replace").splitlines():
                    try:
                        entry = json.loads(line)
                    except ValueError:
                        continue
                    text = entry.get("summary") or entry.get("text") or ""
                    if text:
                        print(f"[factory panel] {text}", flush=True)
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
