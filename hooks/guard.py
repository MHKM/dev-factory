#!/usr/bin/env python3
"""factory guard: PreToolUse hook on Bash.

Only acts in projects that have .factory/. Blocks (exit 2) what no agent may
do: integrate into protected branches (main branch and release/*), merge PRs,
commit directly on them and, except for the developer, switch branches.
It is the first barrier; the real one is branch protection on GitHub.
Messages are in Spanish because they are shown to the human.
"""
from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

FACTORY_AGENTS = ("orchestrator", "analyst", "prototyper", "architect", "developer", "validator")


def block(reason: str) -> None:
    print(f"Bloqueado por la guardia de factory: {reason}", file=sys.stderr)
    sys.exit(2)


def main_branch(root: Path) -> str:
    try:
        text = (root / ".factory" / "project.md").read_text(encoding="utf-8")
        m = re.search(r"^main_branch:\s*(\S+)", text, re.M)
        if m:
            return m.group(1)
    except OSError:
        pass
    return "master"


def current_branch(cwd: str) -> str:
    r = subprocess.run(["git", "branch", "--show-current"], cwd=cwd,
                       capture_output=True, text=True)
    return r.stdout.strip()


def tokens(segment: str) -> list:
    try:
        t = shlex.split(segment)
    except ValueError:
        t = segment.split()
    while t and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", t[0]):
        t.pop(0)
    return t


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    command = (data.get("tool_input") or {}).get("command") or ""
    cwd = data.get("cwd") or os.getcwd()
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or cwd)
    if not (root / ".factory").is_dir():
        return

    main = main_branch(root)
    agent = data.get("agent_type") or ""
    is_factory = agent.startswith("factory:") or agent in FACTORY_AGENTS
    is_developer = agent.endswith("developer")

    def protected(branch: str) -> bool:
        branch = branch.lstrip("+").replace("refs/heads/", "")
        return branch in (main, "master", "main") or branch.startswith("release/")

    current = None

    for segment in re.split(r"&&|\|\||;|\||\n", command):
        t = tokens(segment.strip())
        if not t:
            continue

        if t[0] == "gh":
            if t[1:3] == ["pr", "merge"]:
                block("ningún agente fusiona PRs; la fusión la aprueba y hace el humano.")
            if len(t) > 1 and t[1] == "api" and "merge" in segment:
                block("ningún agente fusiona vía API de GitHub.")
            continue

        if t[0] != "git":
            continue
        i = 1
        while i < len(t) and t[i].startswith("-"):
            i += 2 if t[i] in ("-C", "-c") else 1
        if i >= len(t):
            continue
        sub, args = t[i], t[i + 1:]
        if current is None:
            current = current_branch(cwd)

        if sub == "push":
            if "--all" in args or "--mirror" in args:
                block("push masivo (--all/--mirror) no permitido.")
            refs = [x for x in args if not x.startswith("-")][1:]
            if not refs and protected(current):
                block(f"push a la rama protegida '{current}'.")
            for ref in refs:
                target = ref.split(":", 1)[1] if ":" in ref else ref
                if target in ("HEAD", "+HEAD"):
                    target = current
                if protected(target):
                    block(f"push a la rama protegida '{target}'. Usa una rama de tarea y PR.")
        elif sub in ("merge", "rebase", "cherry-pick", "revert") and protected(current):
            if not any(x in args for x in ("--abort", "--quit")):
                block(f"'git {sub}' sobre la rama protegida '{current}'. "
                      "Integrar en ella lo decide el humano.")
        elif sub == "pull" and protected(current) and "--ff-only" not in args:
            block(f"en la rama protegida '{current}' solo se permite 'git pull --ff-only'.")
        elif sub == "commit" and protected(current) and is_factory:
            block(f"commit directo en la rama protegida '{current}'. Crea una rama de tarea.")
        elif sub in ("checkout", "switch") and is_factory and not is_developer:
            block("solo el desarrollador cambia de rama. Lee otras ramas con "
                  "'git show <rama>:<ruta>', 'git grep <texto> <rama>', "
                  "'git diff <base>...<rama>' o 'factory export <rama>'.")


if __name__ == "__main__":
    main()
