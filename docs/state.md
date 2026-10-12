# Estado: modelo de datos y comando `factory`

El estado de un proyecto vive en `.factory/` (local, sin versionar). Los agentes solo lo leen y lo cambian con el comando `factory` (`bin/factory`). Si mañana el backend pasa a ser GitHub Projects, solo cambia lo que hay debajo de este comando.

Los identificadores (comandos, campos, valores, carpetas) están en inglés. Los mensajes que imprime el comando, en español.

## Estructura

```
.factory/
  project.md             perfil del proyecto + estado del proyecto (ID «project»)
  state/
    M01-web-basica.md    hito (milestone)
    F001-catalogo.md     funcionalidad (feature)
    T001-repo-y-ci.md    tarea (task)
  artifacts/
    vision.md  roadmap.md  architecture.md
    M01/   design.md  batch.md
    F001/  spec.md  business-rules.md  mockup/index.html  design.md  validation.md
    T001/  review.md
  decisions/
    D001-stack-web.md
  tmp/                   exportaciones de ramas (factory export)
  panel.url              URL del panel mientras está en marcha
```

La ruta de los artefactos es fija por convención; no se guarda en el estado. `factory paths <ID>` la muestra.

## Ficheros de estado

Cada elemento es un `.md` con frontmatter plano (valores simples o listas `[a, b]`) y un cuerpo con secciones fijas:

```markdown
---
id: T003
type: task
title: Formulario de cita
kind: technical
parent: F002
milestone: M01
package: P2
phase: in_review
status: waiting_human
reason: Fusionar PR #7
agent: developer
attempts: 1
depends_on: [T001]
branch: task/T003-formulario-de-cita
pr: 7
review: ok
created: 2026-10-12 18:22
updated: 2026-10-12 19:05
---

# T003 · Formulario de cita

## Description
<lo que escribió el arquitecto: objetivo, criterios que cubre, ficheros, interfaces>

## Pending questions

## Resolved questions

## History
- 2026-10-12 18:22 · creado
- …
```

### Campos por tipo

| Tipo | Campos propios |
|---|---|
| project | `name`, `description`, `main_branch`, `remote` (`github`/`none`), `interface` (`web`/`none`/`mixed`), `language` (`es` por defecto), `max_attempts`, `discovery` (`pending`/`done`), `architecture` (`pending`/`done`) |
| milestone | `goal`, `branch` (release), `planned` (`yes`/`no`), `closing` (`requested`/`merged`), `pr` |
| feature | `milestone`, `priority` (`must`/`should`/`later`), `version`, `depends_on`, `needs_mockup` (`yes`/`no`), `validation` (`ko`/`rejected`/vacío) |
| task | `kind` (`technical`/`cross_cutting`/`fix`/`hotfix`), `parent`, `milestone`, `package`, `agent`, `attempts`, `depends_on`, `branch`, `pr`, `review` (`ok`/`ko`) |

Todos tienen además `id`, `type`, `title`, `phase`, `status`, `reason`, `created` y `updated`.

### Fases y situaciones

| Tipo | Fases (`phase`) | En el modelo |
|---|---|---|
| milestone | `proposed` → `approved` → `closed` | Propuesto → Aprobado → Cerrado |
| feature | `defined` → `specified` → `building` → `validated` → `accepted` · laterales: `postponed`, `discarded` | Definida → Especificada → En construcción → Validada → Aceptada · Aplazada, Descartada |
| task | `pending` → `development` → `in_review` → `done` · lateral: `discarded` | Pendiente → Desarrollo → En revisión → Hecha · Descartada |

Situación (`status`): `queued` (en cola) · `in_progress` (en curso) · `waiting_human` (esperando humano) · `blocked` (bloqueada). Las fases terminales no tienen situación.

`factory phase` deja la situación en `queued` salvo que se indique otra con `--status`. Así, al avanzar de fase, el elemento queda listo para el siguiente agente.

IDs: `M01` (hito), `F001` (funcionalidad), `T001` (tarea), `D001` (decisión), `project` (el proyecto). Criterios de aceptación: `AC-F001-01`. Ramas: `release/M01-<slug>` y `task/T001-<slug>`.

## Comandos

| Comando | Para qué |
|---|---|
| `factory init --name N [--branch R] [--language es]` | Crea `.factory/`, inicializa git si hace falta, añade `.factory/` al `.gitignore` y hace el commit inicial si el repo está vacío |
| `factory new milestone\|feature\|task --title T [--text -] …` | Crea un elemento e imprime su ID. `feature` necesita `--milestone`; `task` necesita `--parent` (salvo `--kind hotfix`). Otros: `--goal`, `--priority`, `--kind`, `--package`, `--depends` |
| `factory phase ID PHASE [--status S] [--reason M]` | Cambia la fase |
| `factory status ID S [--reason M]` | Cambia la situación |
| `factory set ID campo=valor …` | Cambia otros campos (no `id`, `type`, `phase` ni `status`) |
| `factory show ID` · `factory paths ID` | Muestra el elemento y sus artefactos |
| `factory list [--type] [--milestone] [--phase] [--status]` | Lista filtrada |
| `factory board` | Progreso: hitos → funcionalidades → tareas |
| `factory attention` | Lo que espera al humano o está bloqueado, con las preguntas |
| `factory next` | Qué toca hacer ahora (ver abajo) |
| `factory ask ID --text - [--agent A] [--reason M]` | Añade preguntas y pasa a `waiting_human` |
| `factory decision --title T [--ref ID] --text -` | Registra una decisión e imprime su ID (`D###`) |
| `factory resolve ID --decision D###` | Mueve las preguntas a «resueltas» y vuelve a `queued` |
| `factory attempt ID [--reason M]` | Suma un intento y bloquea al llegar a `max_attempts` |
| `factory open-release M##` | Crea `release/M##-…` desde la rama principal (y la sube si hay GitHub) |
| `factory export REF` | Exporta una rama a `.factory/tmp/<ref>/` para leerla o probarla sin cambiar de rama |
| `factory sync` | Detecta PRs o ramas fusionadas: tareas a `done` y hitos a `closed` |
| `factory panel [--port 8765] [--open]` | Sirve el panel de control en `http://127.0.0.1:<puerto>/` (si está ocupado, prueba los siguientes) y guarda la URL en `.factory/panel.url` |

`--text -` lee de la entrada estándar (heredoc).

## Enrutado: `factory next`

Calcula qué hacer a partir del estado. El orquestador lo ejecuta en cada vuelta de su bucle. Primero lista lo que espera al humano y lo que está en curso; después, las acciones, con la forma `<who> <ID(s)> <mode>`. Un elemento en `in_progress`, `waiting_human` o `blocked` no genera acciones.

| Condición | Quién | Modo |
|---|---|---|
| `discovery` pendiente | orchestrator | `discovery` |
| `architecture` pendiente | architect | `base` |
| Ningún hito aprobado y hay uno propuesto | orchestrator | `approve_milestone_first` (primera vez, con visión, roadmap y arquitectura) o `approve_milestone` |
| Hito aprobado sin `branch` | orchestrator | `open_release` |
| Hito aprobado sin `planned=yes` | architect | `milestone` |
| Feature `defined` sin `spec.md` | analyst | `specify` |
| Feature `defined` con spec, `needs_mockup=yes` y sin maqueta | prototyper | `mockup` |
| Feature `defined` con todo listo | orchestrator | `approve_spec` |
| Feature `specified` | architect | `feature` |
| Feature `building` con `validation` ko/rejected y sin tareas abiertas | architect | `fix` |
| Feature `building` con todas sus tareas en `done` | validator | `feature_validation` |
| Task `pending` (o `development` en cola) con dependencias cumplidas y ningún developer trabajando | developer | `implement` / `resume` / `hotfix` (el paquete entero si lo tiene); **solo una a la vez**: primero hotfix, luego transversales, luego por ID |
| Task `in_review` sin `review=ok` | validator | `task_review` |
| Task `in_review` con `review=ok` | orchestrator | `approve_merge` |
| Todas las features vivas `validated`/`accepted` (al menos una `validated`) y tareas hechas | orchestrator | `present_batch` |
| Todas las features vivas `accepted` | orchestrator | `close_milestone` |
| No quedan hitos | orchestrator | `roadmap_review` |

Modos que no salen de `factory next` y lanza el orquestador según la situación: `revise_spec` (analyst, prototyper) y `change_request` (analyst).

Un hito activo a la vez (una release). Las dependencias se cumplen cuando el elemento está `done`, `validated` o `accepted`.
