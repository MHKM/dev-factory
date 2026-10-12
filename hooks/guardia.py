#!/usr/bin/env python3
"""Guardia de la plataforma: hook PreToolUse sobre Bash.

Solo actúa en proyectos con .factory/. Bloquea (exit 2) lo que ningún agente
puede hacer: integrar en ramas protegidas (rama principal y release/*), fusionar
PRs, commitear directamente en ellas y, salvo el desarrollador, cambiar de rama.
Es la primera barrera; la real es la protección de rama en GitHub.
"""
from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path


def bloquear(motivo: str) -> None:
    print(f"Bloqueado por la guardia de factory: {motivo}", file=sys.stderr)
    sys.exit(2)


def rama_principal(raiz: Path) -> str:
    try:
        texto = (raiz / ".factory" / "proyecto.md").read_text(encoding="utf-8")
        m = re.search(r"^rama_principal:\s*(\S+)", texto, re.M)
        if m:
            return m.group(1)
    except OSError:
        pass
    return "master"


def rama_actual(cwd: str) -> str:
    r = subprocess.run(["git", "branch", "--show-current"], cwd=cwd,
                       capture_output=True, text=True)
    return r.stdout.strip()


def tokens(segmento: str) -> list:
    try:
        t = shlex.split(segmento)
    except ValueError:
        t = segmento.split()
    while t and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", t[0]):
        t.pop(0)
    return t


def main() -> None:
    try:
        datos = json.load(sys.stdin)
    except ValueError:
        return
    comando = (datos.get("tool_input") or {}).get("command") or ""
    cwd = datos.get("cwd") or os.getcwd()
    raiz = Path(os.environ.get("CLAUDE_PROJECT_DIR") or cwd)
    if not (raiz / ".factory").is_dir():
        return

    principal = rama_principal(raiz)
    agente = datos.get("agent_type") or ""
    es_factory = agente.startswith("factory:") or agente in (
        "orquestador", "analista", "prototipador", "arquitecto", "desarrollador", "validador")
    es_desarrollador = agente.endswith("desarrollador")

    def protegida(rama: str) -> bool:
        rama = rama.lstrip("+").replace("refs/heads/", "")
        return rama in (principal, "master", "main") or rama.startswith("release/")

    actual = None

    for segmento in re.split(r"&&|\|\||;|\||\n", comando):
        t = tokens(segmento.strip())
        if not t:
            continue

        if t[0] == "gh":
            if t[1:3] == ["pr", "merge"]:
                bloquear("ningún agente fusiona PRs; la fusión la aprueba y hace el humano.")
            if len(t) > 1 and t[1] == "api" and "merge" in segmento:
                bloquear("ningún agente fusiona vía API de GitHub.")
            continue

        if t[0] != "git":
            continue
        i = 1
        while i < len(t) and t[i].startswith("-"):
            i += 2 if t[i] in ("-C", "-c") else 1
        if i >= len(t):
            continue
        sub, args = t[i], t[i + 1:]
        if actual is None:
            actual = rama_actual(cwd)

        if sub == "push":
            if "--all" in args or "--mirror" in args:
                bloquear("push masivo (--all/--mirror) no permitido.")
            refs = [x for x in args if not x.startswith("-")][1:]
            if not refs:
                if protegida(actual):
                    bloquear(f"push a la rama protegida '{actual}'.")
            for ref in refs:
                destino = ref.split(":", 1)[1] if ":" in ref else ref
                if destino in ("HEAD", "+HEAD"):
                    destino = actual
                if protegida(destino):
                    bloquear(f"push a la rama protegida '{destino}'. Usa una rama de tarea y PR.")
        elif sub in ("merge", "rebase", "cherry-pick", "revert") and protegida(actual):
            if not any(x in args for x in ("--abort", "--quit")):
                bloquear(f"'git {sub}' sobre la rama protegida '{actual}'. "
                         "Integrar en ella lo decide el humano.")
        elif sub == "pull" and protegida(actual) and "--ff-only" not in args:
            bloquear(f"en la rama protegida '{actual}' solo se permite 'git pull --ff-only'.")
        elif sub == "commit" and protegida(actual) and es_factory:
            bloquear(f"commit directo en la rama protegida '{actual}'. Crea una rama de tarea.")
        elif sub in ("checkout", "switch") and es_factory and not es_desarrollador:
            bloquear("solo el desarrollador cambia de rama. Lee otras ramas con "
                     "'git show <rama>:<ruta>', 'git grep <texto> <rama>', "
                     "'git diff <base>...<rama>' o 'factory exportar <rama>'.")


if __name__ == "__main__":
    main()
