# dev-factory

Plataforma de desarrollo agéntico sobre Claude Code. Le cuentas a un orquestador lo que quieres construir; él te ayuda a definirlo y coordina agentes especializados (analista, prototipador, arquitecto, desarrollador, validador). Solo te pide intervenir en los puntos de decisión.

```bash
cd <carpeta-del-proyecto-nuevo>
claude --plugin-dir ~/Documents/projects/dev-factory --agent factory:orchestrator "arranca"
```

## Contenido

| Ruta | Qué es |
|---|---|
| `docs/platform-model.md` | Modelo de diseño y decisiones |
| `docs/usage.md` | Cómo arrancar, qué esperar, dónde mirar |
| `docs/state.md` | Modelo de datos de `.factory/`, comando `factory` y reglas de enrutado |
| `agents/` | Orquestador y subagentes por rol |
| `skills/discovery/` | Modo conversacional de descubrimiento del orquestador |
| `shared/agent-rules.md` | Reglas compartidas por todos los agentes |
| `templates/` | Plantillas de artefactos |
| `bin/factory` | Capa de estado (CLI, Python sin dependencias) y servidor del panel |
| `panel/index.html` | Panel de control: vistas Producto y Construcción |
| `hooks/` | Guardia de ramas |
| `.claude-plugin/` | Manifiesto del plugin y marketplace local |

El código y el modelo de datos de la plataforma están en inglés; los textos para el humano, en español.
