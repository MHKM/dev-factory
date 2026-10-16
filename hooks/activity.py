#!/usr/bin/env python3
"""factory activity tracker: hook for SessionStart, SubagentStart, SubagentStop and PreToolUse.

Keeps .factory/activity.json up to date with the factory agents that are working,
the items they work on and their last action, so the panel can show them without
relying on agents to report themselves. Never blocks anything.
"""
from __future__ import annotations

import fcntl
import json
import os
import re
import shlex
import sys
import time
from pathlib import Path

RECENT_LIMIT = 10


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def describe(tool: str, tool_input: dict) -> dict:
    """Short, language-neutral description of a tool call; the panel localises it."""
    target = ""
    if tool in ("Edit", "Write", "Read", "NotebookEdit"):
        target = Path(tool_input.get("file_path") or "").name
    elif tool == "Bash":
        target = tool_input.get("description") or (tool_input.get("command") or "")[:80]
    elif tool in ("Grep", "Glob"):
        target = tool_input.get("pattern") or ""
    elif tool in ("WebFetch", "WebSearch"):
        target = tool_input.get("url") or tool_input.get("query") or ""
    return {"tool": tool, "target": str(target)[:120]}


def normalize(ident: str) -> str:
    """Same spelling the state uses: lowercase for project/design, uppercase for IDs."""
    return ident.lower() if ident.lower() in ("project", "design") else ident.upper()


def items_from_command(command: str) -> list:
    """IDs an agent puts in progress through the factory CLI."""
    found = []
    for segment in re.split(r"&&|\|\||;|\n", command):
        try:
            t = shlex.split(segment)
        except ValueError:
            continue
        if len(t) < 3 or Path(t[0]).name != "factory":
            continue
        if t[1] == "status" and len(t) >= 4 and t[3] == "in_progress":
            found.append(normalize(t[2]))
        elif t[1] == "phase" and "--status" in t and "in_progress" in t:
            found.append(normalize(t[2]))
    return found


def update(act: dict, data: dict) -> bool:
    agents = act.setdefault("agents", {})
    recent = act.setdefault("recent", [])
    event = data.get("hook_event_name") or ""
    agent_id = data.get("agent_id") or ""
    agent_type = data.get("agent_type") or ""
    session = data.get("session_id") or ""

    if event == "SessionStart":
        stale = [k for k, v in agents.items() if v.get("session") != session]
        for k in stale:
            agents.pop(k)
        return bool(stale)

    if not agent_id or not agent_type.startswith("factory:"):
        return False
    role = agent_type.split(":")[-1]

    if event == "SubagentStart":
        agents[agent_id] = {"role": role, "session": session, "started": now(),
                            "last_seen": now(), "items": [], "action": {"tool": "start"}}
        return True

    if event == "SubagentStop":
        entry = agents.pop(agent_id, None)
        if entry:
            recent.insert(0, {"role": role, "items": entry.get("items", []),
                              "started": entry.get("started"), "ended": now()})
            del recent[RECENT_LIMIT:]
        return True

    if event == "PreToolUse":
        entry = agents.setdefault(agent_id, {"role": role, "session": session, "started": now(),
                                             "items": []})
        tool = data.get("tool_name") or ""
        tool_input = data.get("tool_input") or {}
        entry["last_seen"] = now()
        entry["action"] = describe(tool, tool_input)
        if tool == "Bash":
            for ident in items_from_command(tool_input.get("command") or ""):
                if ident not in entry["items"]:
                    entry["items"].append(ident)
        return True
    return False


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd())
    fac = root / ".factory"
    if not fac.is_dir():
        return
    path = fac / "activity.json"
    with open(fac / ".activity.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            act = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            act = {}
        if update(act, data):
            tmp = path.with_suffix(".tmp")
            tmp.write_text(json.dumps(act, ensure_ascii=False, indent=1), encoding="utf-8")
            os.replace(tmp, path)


if __name__ == "__main__":
    try:
        main()
    except Exception:  # activity tracking must never get in the way
        pass
