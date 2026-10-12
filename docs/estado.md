# Estado: modelo de datos y comando `factory`

El estado de un proyecto vive en `.factory/` (local, sin versionar). Los agentes solo lo leen y lo cambian con el comando `factory` (`bin/factory`). Si mañana el backend pasa a ser GitHub Projects, solo cambia lo que hay debajo de este comando.

## Estructura

```
.factory/
  proyecto.md            perfil del proyecto + estado del proyecto (ID «proyecto»)
  estado/
    H01-web-basica.md    hito
    F001-catalogo.md     funcionalidad
    T001-repo-y-ci.md    tarea
  artefactos/
    vision.md  roadmap.md  arquitectura.md
    H01/   diseno.md  lote.md
    F001/  spec.md  reglas-negocio.md  maqueta/index.html  diseno.md  validacion.md
    T001/  revision.md
  decisiones/
    D001-stack-web.md
  tmp/                   exportaciones de ramas (factory exportar)
```

La ruta de los artefactos es fija por convención; no se guarda en el estado. `factory rutas <ID>` la muestra.

## Ficheros de estado

Cada elemento es un `.md` con frontmatter plano (valores simples o listas `[a, b]`) y un cuerpo con secciones fijas:

```markdown
---
id: T003
tipo: tarea
titulo: Formulario de cita
clase: tecnica
padre: F002
hito: H01
paquete: P2
fase: en_revision
situacion: esperando_humano
motivo: Fusionar PR #7
agente: desarrollador
intentos: 1
depende_de: [T001]
rama: tarea/T003-formulario-de-cita
pr: 7
revision: ok
creado: 2026-10-12 18:22
actualizado: 2026-10-12 19:05
---

# T003 · Formulario de cita

## Descripción
<lo que escribió el arquitecto: objetivo, criterios que cubre, ficheros, interfaces>

## Preguntas pendientes

## Preguntas resueltas

## Historial
- 2026-10-12 18:22 · creado
- …
```

### Campos por tipo

| Tipo | Campos propios |
|---|---|
| proyecto | `nombre`, `descripcion`, `rama_principal`, `remoto` (`github`/`ninguno`), `interfaz` (`web`/`ninguna`/`mixta`), `max_intentos`, `descubrimiento` (`pendiente`/`hecho`), `arquitectura` (`pendiente`/`hecha`) |
| hito | `objetivo`, `rama` (release), `planificado` (`si`/`no`), `cierre` (`solicitado`/`fusionado`), `pr` |
| func | `hito`, `prioridad`, `version`, `depende_de`, `necesita_maqueta` (`si`/`no`), `validacion` (`ko`/`rechazada`/vacío) |
| tarea | `clase` (`tecnica`/`transversal`/`correccion`/`hotfix`), `padre`, `hito`, `paquete`, `agente`, `intentos`, `depende_de`, `rama`, `pr`, `revision` (`ok`/`ko`) |

Todos tienen además `id`, `tipo`, `titulo`, `fase`, `situacion`, `motivo`, `creado` y `actualizado`.

### Fases y situaciones

| Tipo | Fases |
|---|---|
| hito | `propuesto` → `aprobado` → `cerrado` |
| func | `definida` → `especificada` → `en_construccion` → `validada` → `aceptada` · laterales: `aplazada`, `descartada` |
| tarea | `pendiente` → `desarrollo` → `en_revision` → `hecha` · lateral: `descartada` |

Situación: `en_cola` · `en_curso` · `esperando_humano` · `bloqueada`. Las fases terminales no tienen situación.

`factory fase` deja la situación en `en_cola` salvo que se indique otra con `--situacion`. Así, al avanzar de fase, el elemento queda listo para el siguiente agente.

## Comandos

| Comando | Para qué |
|---|---|
| `factory init --nombre N [--rama R]` | Crea `.factory/`, inicializa git si hace falta, añade `.factory/` al `.gitignore` y hace el commit inicial si el repo está vacío |
| `factory nuevo hito\|func\|tarea --titulo T [--texto -] …` | Crea un elemento e imprime su ID. `func` necesita `--hito`; `tarea` necesita `--padre` (salvo `--clase hotfix`) |
| `factory fase ID FASE [--situacion S] [--motivo M]` | Cambia la fase |
| `factory situacion ID S [--motivo M]` | Cambia la situación |
| `factory set ID campo=valor …` | Cambia otros campos (no `id`, `tipo`, `fase` ni `situacion`) |
| `factory ver ID` · `factory rutas ID` | Muestra el elemento y sus artefactos |
| `factory lista [--tipo] [--hito] [--fase] [--situacion]` | Lista filtrada |
| `factory tablero` | Progreso: hitos → funcionalidades → tareas |
| `factory atencion` | Lo que espera al humano o está bloqueado, con las preguntas |
| `factory siguiente` | Qué toca hacer ahora (ver abajo) |
| `factory preguntar ID --texto - [--agente A] [--motivo M]` | Añade preguntas y pasa a `esperando_humano` |
| `factory decision --titulo T [--ref ID] --texto -` | Registra una decisión e imprime su ID (`D###`) |
| `factory resolver ID --decision D###` | Mueve las preguntas a «resueltas» y vuelve a `en_cola` |
| `factory intento ID [--motivo M]` | Suma un intento y bloquea al llegar a `max_intentos` |
| `factory abrir-release H##` | Crea `release/H##-…` desde la rama principal (y la sube si hay GitHub) |
| `factory exportar REF` | Exporta una rama a `.factory/tmp/<ref>/` para leerla o probarla sin cambiar de rama |
| `factory sync` | Detecta PRs o ramas fusionadas: tareas a `hecha` y hitos a `cerrado` |

`--texto -` lee de la entrada estándar (heredoc).

## Enrutado: `factory siguiente`

Calcula qué hacer a partir del estado. El orquestador lo ejecuta en cada vuelta de su bucle. Primero lista lo que espera al humano y lo que está en curso; después, las acciones. Un elemento en `en_curso`, `esperando_humano` o `bloqueada` no genera acciones.

| Condición | Acción |
|---|---|
| `descubrimiento` pendiente | orquestador: descubrimiento |
| `arquitectura` pendiente | arquitecto, modo base |
| Ningún hito aprobado y hay uno propuesto | orquestador: pedir aprobación del hito (la primera vez, con visión, roadmap y arquitectura) |
| Hito aprobado sin `rama` | orquestador: abrir release |
| Hito aprobado sin `planificado=si` | arquitecto, modo hito (tareas transversales) |
| Func `definida` sin `spec.md` | analista: especificar |
| Func `definida` con spec, `necesita_maqueta=si` y sin maqueta | prototipador |
| Func `definida` con todo listo | orquestador: presentar especificación |
| Func `especificada` | arquitecto, modo funcionalidad |
| Func `en_construccion` con `validacion` ko/rechazada y sin tareas abiertas | arquitecto, modo corrección |
| Func `en_construccion` con todas sus tareas hechas | validador, modo funcionalidad |
| Tarea `pendiente` (o `desarrollo` en cola) con dependencias hechas y ningún desarrollador trabajando | desarrollador (el paquete entero si lo tiene); **solo una a la vez**: primero hotfix, luego transversales, luego por ID |
| Tarea `en_revision` sin `revision=ok` | validador, modo tarea |
| Todas las funcs vivas validadas o aceptadas (al menos una validada) y tareas hechas | orquestador: preparar lote |
| Todas las funcs vivas aceptadas | orquestador: cerrar hito (fusión de la release) |
| No quedan hitos | orquestador: revisión de roadmap |

Un hito activo a la vez (una release). Las dependencias se cumplen cuando el elemento está `hecha`, `validada` o `aceptada`.
