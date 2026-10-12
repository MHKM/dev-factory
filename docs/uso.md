# Uso

## Requisitos

- Claude Code (probado con 2.1.296).
- `python3` (3.9 o superior) y `git`.
- `gh` autenticado (`gh auth status`) si el proyecto va a tener repositorio en GitHub.

## Arrancar un proyecto

Cada construcción va en **su propia carpeta**, fuera de este repositorio:

```bash
mkdir ~/Documents/projects/web-taller && cd ~/Documents/projects/web-taller
claude --plugin-dir ~/Documents/projects/dev-factory --agent factory:orquestador
```

Para no escribirlo cada vez:

```bash
alias factory-start='claude --plugin-dir ~/Documents/projects/dev-factory --agent factory:orquestador'
```

`--plugin-dir` carga el plugin desde este repositorio tal como esté en disco, así que cualquier cambio en agentes, plantillas o en el comando se aplica en la siguiente sesión. Alternativa estable: instalarlo desde el marketplace local (`/plugin marketplace add ~/Documents/projects/dev-factory` y después instalar `factory`) y arrancar solo con `claude --agent factory:orquestador`.

Para retomar un proyecto, se arranca igual en su carpeta: el orquestador lee `.factory/`, sincroniza y resume dónde estáis.

## Qué esperar (ejemplo)

> «Quiero construir una web para el taller de mi primo, en Boadilla. Que permita ver los servicios que ofrece y un formulario para que le llamen para cita.»

1. **Inicio**: te pregunta el nombre del proyecto y si quieres repositorio en GitHub o solo local. Crea `.factory/` y el commit inicial.
2. **Descubrimiento**: varias rondas cortas sobre servicios, precios, cómo quiere recibir las peticiones, fotos y logo, horario y ubicación. Propone ideas (mapa, botón de WhatsApp, aviso de privacidad…). Al final escribe la visión y el roadmap, y crea los hitos y funcionalidades.
3. **Arquitectura base**: el arquitecto te propone el stack con 2 o 3 opciones (por ejemplo, una web estática con un servicio de formularios frente a algo con backend). Tú eliges.
4. **Aprobar el hito**: resumen de visión, roadmap y arquitectura, y el contenido del primer hito. Al aprobarlo se crea `release/H01-…`.
5. **Especificación y maqueta**: el analista escribe las especificaciones y el prototipador las maquetas HTML. Te las presenta una a una; puedes abrir la maqueta en el navegador.
6. **Construcción**: el arquitecto diseña y crea las tareas. El desarrollador las hace una a una (tests primero) y abre PRs contra la release. El validador revisa cada PR. Tú fusionas.
7. **Validación y lote**: con todas las tareas fusionadas, el validador comprueba los criterios en la release. Después te presenta el lote para aceptar cada funcionalidad.
8. **Cierre**: PR de la release a `master`; la fusionas y el hito queda cerrado.

## Dónde mirar

| Para | Comando o ruta |
|---|---|
| Qué espera de ti | `factory atencion` |
| Progreso | `factory tablero` |
| Qué toca ahora | `factory siguiente` |
| Un elemento | `factory ver F001` |
| Artefactos | `.factory/artefactos/` |
| Decisiones | `.factory/decisiones/` |

`factory` solo está en el PATH de los agentes de una sesión con el plugin cargado. Desde tu terminal, o con `!` dentro de la sesión, usa la ruta completa: `~/Documents/projects/dev-factory/bin/factory tablero`. También puedes pedírselo al orquestador («enséñame el tablero»).

## Fusiones

- **Con GitHub**: fusionas las PRs en la web. En repos privados con cuenta gratuita no hay protección de rama, así que la única barrera es la guardia local.
- **En local**: el orquestador te da el comando para ejecutarlo tú con `!` (por ejemplo, `! git switch release/H01-… && git merge --no-ff tarea/T003-…`).

En ambos casos, al volver el orquestador ejecuta `factory sync` y detecta la fusión.

## Guardia (hook)

Solo actúa en carpetas con `.factory/`. Bloquea a cualquier agente:

- el push a la rama principal o a `release/*`, y el push con `--all`/`--mirror`;
- `merge`/`rebase`/`cherry-pick`/`revert` sobre esas ramas;
- `pull` sin `--ff-only` sobre esas ramas;
- `gh pr merge` y las fusiones vía `gh api`.

Además, a los agentes de factory:

- el commit directo en ramas protegidas;
- el `checkout`/`switch` a todos menos al desarrollador.

Los comandos que ejecutas tú con `!` no pasan por la guardia.

**Limitación conocida**: en un comando encadenado (`git switch X && git merge Y`), la guardia evalúa la rama actual antes del `switch`.

## Empezar de cero

Borrar `.factory/` reinicia el estado del proyecto (no el código). No hay papelera: los artefactos no están versionados.

## Ajustes rápidos

- **Modelos y esfuerzo**: en el frontmatter de `agents/*.md`.
- **Intentos máximos**: `factory set proyecto max_intentos=N`.
- **Comportamiento de un rol**: su `agents/<rol>.md`. Las reglas compartidas, en `comun/reglas-agentes.md`.
