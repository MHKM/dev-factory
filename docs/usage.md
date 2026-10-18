# Uso

## Requisitos

- Claude Code (probado con 2.1.296).
- `python3` (3.9 o superior) y `git`.
- `gh` autenticado (`gh auth status`) si el proyecto va a tener repositorio en GitHub.

## Arrancar un proyecto

Cada construcción va en **su propia carpeta**, fuera de este repositorio.

**Instalación (una vez):** el plugin se instala desde el marketplace local de este repo y queda disponible en cualquier sesión de `claude`:

```bash
claude plugin marketplace add ~/Documents/projects/dev-factory
claude plugin install factory@dev-factory
```

Se carga desde este repositorio tal como esté en disco, así que los cambios en agentes, plantillas o el comando se aplican en la siguiente sesión.

**Arrancar:** abre `claude` en la carpeta del proyecto y escribe

```
/factory:start
```

La sesión adopta el rol de orquestador: en un proyecto nuevo te pregunta qué quieres construir; en uno existente resume el estado y abre el panel. `/factory:start` también sirve en mitad de una sesión para volver a ver el estado.

**Alternativa estricta:** `~/Documents/projects/dev-factory/factory-start` abre la sesión con el orquestador como agente principal, lo que además aplica sus restricciones de herramientas (por ejemplo, no puede editar código él mismo). Admite opciones de `claude` delante (`factory-start --model sonnet`).

Para retomar un proyecto, se arranca igual en su carpeta: el orquestador lee `.factory/`, sincroniza y resume dónde estáis.

### Permisos

Los agentes ejecutan `factory` constantemente. Para que Claude Code no pida aprobación en cada llamada, permite el comando en tu `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(factory:*)",
      "Read(//ruta/a/dev-factory/**)"
    ]
  }
}
```

La segunda regla deja leer las instrucciones y las reglas del plugin (fuera de la carpeta del proyecto) sin pedir permiso.

## Qué esperar (ejemplo)

> «Quiero construir una web para el taller de mi primo, en Boadilla. Que permita ver los servicios que ofrece y un formulario para que le llamen para cita.»

1. **Inicio**: te pregunta el nombre del proyecto, si quieres repositorio en GitHub (privado o público) o solo local, y el idioma de la interfaz (español o inglés: panel, mensajes, documentos y conversación; el código va siempre en inglés). Crea `.factory/`, hace el commit inicial y abre el panel.
2. **Descubrimiento**: varias rondas cortas sobre servicios, precios, cómo quiere recibir las peticiones, fotos y logo, horario y ubicación. Propone ideas (mapa, botón de WhatsApp, aviso de privacidad…). Al final escribe la visión y el roadmap, y crea los hitos y funcionalidades.
3. **Arquitectura base**: el arquitecto te propone el stack con 2 o 3 opciones (por ejemplo, una web estática con un servicio de formularios frente a algo con backend). Tú eliges.
4. **Cómo se diseña** (proyectos con interfaz): te pregunta el nivel (kit completo de agencia, solo directrices o sin diseño), dónde se diseña (lienzo de Claude Design o maquetas locales, si tiene el lienzo disponible), qué plugin de diseño usar (si hay alguno instalado, como `frontend-design`) y si ya tienes logo, colores o fotos. Con maquetas locales, el prototipador crea primero el kit y lo apruebas.
5. **Aprobar el hito**: resumen de visión, roadmap y arquitectura, y el contenido del primer hito. Al aprobarlo empieza su definición.
6. **Especificaciones**: el analista las escribe y apruebas cada una en el panel.
7. **Diseño del hito** (si tiene pantallas): con Claude Design, el orquestador busca material real del cliente, te pide lo que falte y diseña las pantallas contigo en un lienzo de claude.ai (en el primer hito, 2-3 direcciones y variantes con y sin tus fotos). Puedes retocar a mano en el lienzo. Al aprobarlo, se baja a local: una maqueta por funcionalidad y el kit al día. Con maquetas locales, las hace el prototipador y las apruebas igual.
8. **Comenzar construcción**: botón del hito en el panel (o automático). Se crea `release/M01-…` y el arquitecto diseña y crea las tareas. El desarrollador las hace una a una (tests primero) y abre PRs contra la release. El validador revisa cada PR. Tú fusionas.
9. **Validación y lote**: con todas las tareas fusionadas, el validador comprueba los criterios en la release. Después te presenta el lote para aceptar cada funcionalidad.
10. **Cierre**: PR de la release a `master`; la fusionas y el hito queda cerrado.

## Panel de control

Al arrancar, el orquestador abre el panel en el navegador (`http://127.0.0.1:8765/` o el siguiente puerto libre; la URL queda en `.factory/panel.url`). Trabaja con la terminal y el panel a la vez:

- **Producto**: lo definido y lo aprobado, con los tres OK de cada funcionalidad y acceso a especificaciones, maquetas, diseños, validaciones y decisiones.
- **Construcción**: lo que te espera (con botón directo a la PR cuando toca fusionar), los agentes trabajando ahora (rol, elementos y última acción, con aviso si un agente lleva más de 5 minutos sin actividad), los próximos pasos, lo terminado recientemente y el kanban de tareas.

### Hitos: definir en paralelo, construir de uno en uno

En la vista Producto cada hito tiene sus botones según su fase: **Iniciar definición** (propuesto), **Comenzar construcción** (activo cuando todas sus especificaciones están aprobadas; si otro se está construyendo, queda en cola), subir/bajar, editar y borrar (solo propuestos y vacíos). Cada funcionalidad tiene **Mover a…** (otro hito o «Más adelante»). Abajo: **+ Nuevo hito** y **+ Nueva funcionalidad** (el orquestador comprueba si encaja o es un cambio de algo ya hecho).

Arriba, el interruptor **Construcción automática**: activado, un hito pasa a construcción en cuanto su definición está aprobada, sin pedirte confirmación.

### Decidir y hablar desde el panel

- **Botones en «Te espera»**: aprobar, pedir cambios (con comentario), aplazar, descartar, «ya la he fusionado», aceptar el lote y las opciones de las preguntas de los agentes. El panel aplica la decisión al momento (estado y registro de decisión) y avisa al orquestador.
- **Diálogo con el orquestador** (abajo): ves sus mensajes y le escribes sin ir a la terminal.
- **Aviso sonoro** (🔔 arriba) cuando aparece algo nuevo que te espera.

Cómo llega al orquestador: un monitor del plugin vigila `.factory/inbox.jsonl` y le pasa cada acción como aviso `[factory panel] …`, que lo despierta. Solo funciona en sesiones interactivas. La sesión sigue viviendo en la terminal: los permisos de herramientas se siguen aprobando allí.

Se actualiza solo. Para levantarlo a mano, desde la carpeta del proyecto: `~/Documents/projects/dev-factory/bin/factory panel --open`. Las maquetas se abren en una pestaña nueva. El renderizado de Markdown usa `marked` desde jsDelivr; sin conexión, los documentos se muestran como texto plano.

## Kit de diseño

Vive en `.factory/artifacts/design/` y es lo que entregaría una agencia:

| Fichero | Qué es |
|---|---|
| `brand-guide.md` | Guía de marca: concepto, logo, color, tipografía, retícula, iconografía, fotografía, componentes, tono de voz, accesibilidad |
| `tokens.json` | Fuente única de los valores, en formato estándar W3C Design Tokens |
| `tokens.css` | Variables CSS generadas (`factory tokens`), con modo oscuro |
| `index.html` | Galería: muestra cada color con HEX, RGB, HSL, CMYK, Pantone y contraste WCAG, la tipografía, el espaciado y los componentes |
| `assets/` | Logos y recursos aportados |

- **Pantone y CMYK** son equivalencias aproximadas: confírmalas con una guía física antes de imprimir.
- **Reutilizar el kit** en otro proyecto: copia la carpeta a `.factory/artifacts/design/` del nuevo proyecto y ajusta `tokens.json`.
- **Paso a código**: en el primer hito, una tarea transversal copia `tokens.json` al repositorio y genera el tema del stack desde él.
- **La galería necesita servirse** (panel o servidor local): abierta como fichero, el navegador bloquea la lectura de `tokens.json`.

## Dónde mirar

| Para | Comando o ruta |
|---|---|
| Visión general | el panel |
| Qué espera de ti | `factory attention` |
| Progreso | `factory board` |
| Qué toca ahora | `factory next` |
| Un elemento | `factory show F001` |
| Artefactos | `.factory/artifacts/` |
| Decisiones | `.factory/decisions/` |

`factory` solo está en el PATH de los agentes de una sesión con el plugin cargado. Desde tu terminal, o con `!` dentro de la sesión, usa la ruta completa: `~/Documents/projects/dev-factory/bin/factory board`. También puedes pedírselo al orquestador («enséñame el tablero»).

## Fusiones

- **Con GitHub**: fusionas las PRs en la web. En repos privados con cuenta gratuita no hay protección de rama, así que la única barrera es la guardia local.
- **En local**: el orquestador te da el comando para ejecutarlo tú con `!` (por ejemplo, `! git switch release/M01-… && git merge --no-ff task/T003-…`).

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
- **Intentos máximos**: `factory set project max_attempts=N`.
- **Idioma de la interfaz**: `factory set project language=en` (o `es`). El panel cambia al momento; los documentos ya escritos no se traducen.
- **Comportamiento de un rol**: su `agents/<rol>.md`. Las reglas compartidas, en `shared/agent-rules.md`.
