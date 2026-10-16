#!/usr/bin/env python3
"""factory guard: PreToolUse hook on Bash.

Only acts in projects that have .factory/. Blocks (exit 2) what no agent may
do: integrate into protected branches (main branch and release/*), merge PRs,
commit directly on them and, except for the developer, switch branches.
It is the first barrier; the real one is branch protection on GitHub.
Messages follow the project's language because they are shown to the human.
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


MESSAGES = {
    "prefix": ("Bloqueado por la guardia de factory: ", "Blocked by the factory guard: "),
    "pr_merge": ("ningún agente fusiona PRs; la fusión la aprueba y hace el humano.",
                 "no agent merges PRs; the human approves and merges."),
    "api_merge": ("ningún agente fusiona vía API de GitHub.", "no agent merges through the GitHub API."),
    "push_all": ("push masivo (--all/--mirror) no permitido.", "bulk push (--all/--mirror) is not allowed."),
    "push_current": ("push a la rama protegida '{b}'.", "push to the protected branch '{b}'."),
    "push_ref": ("push a la rama protegida '{b}'. Usa una rama de tarea y PR.",
                 "push to the protected branch '{b}'. Use a task branch and a PR."),
    "integrate": ("'git {sub}' sobre la rama protegida '{b}'. Integrar en ella lo decide el humano.",
                  "'git {sub}' on the protected branch '{b}'. Integrating into it is the human's call."),
    "pull": ("en la rama protegida '{b}' solo se permite 'git pull --ff-only'.",
             "only 'git pull --ff-only' is allowed on the protected branch '{b}'."),
    "commit": ("commit directo en la rama protegida '{b}'. Crea una rama de tarea.",
               "direct commit on the protected branch '{b}'. Create a task branch."),
    "switch": ("solo el desarrollador cambia de rama. Lee otras ramas con 'git show <rama>:<ruta>', "
               "'git grep <texto> <rama>', 'git diff <base>...<rama>' o 'factory export <rama>'.",
               "only the developer switches branches. Read other branches with 'git show <branch>:<path>', "
               "'git grep <text> <branch>', 'git diff <base>...<branch>' or 'factory export <branch>'."),
}
LANG = "es"


def block(key: str, **kw) -> None:
    pick = 1 if LANG == "en" else 0
    print(MESSAGES["prefix"][pick] + MESSAGES[key][pick].format(**kw), file=sys.stderr)
    sys.exit(2)


def profile_value(root: Path, field: str, default: str) -> str:
    try:
        text = (root / ".factory" / "project.md").read_text(encoding="utf-8")
        m = re.search(rf"^{field}:\s*(\S+)", text, re.M)
        if m:
            return m.group(1)
    except OSError:
        pass
    return default


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

    global LANG
    LANG = profile_value(root, "language", "es")
    main = profile_value(root, "main_branch", "master")
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
                block("pr_merge")
            if len(t) > 1 and t[1] == "api" and "merge" in segment:
                block("api_merge")
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
                block("push_all")
            refs = [x for x in args if not x.startswith("-")][1:]
            if not refs and protected(current):
                block("push_current", b=current)
            for ref in refs:
                target = ref.split(":", 1)[1] if ":" in ref else ref
                if target in ("HEAD", "+HEAD"):
                    target = current
                if protected(target):
                    block("push_ref", b=target)
        elif sub in ("merge", "rebase", "cherry-pick", "revert") and protected(current):
            if not any(x in args for x in ("--abort", "--quit")):
                block("integrate", sub=sub, b=current)
        elif sub == "pull" and protected(current) and "--ff-only" not in args:
            block("pull", b=current)
        elif sub == "commit" and protected(current) and is_factory:
            block("commit", b=current)
        elif sub in ("checkout", "switch") and is_factory and not is_developer:
            block("switch")


if __name__ == "__main__":
    main()
