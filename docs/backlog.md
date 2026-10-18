# Backlog de la plataforma

Lo pendiente para cerrar dev-factory. Cada elemento dice si se puede avanzar **sin ti** o necesita tu **atención**.

## Reglas para el trabajo sin ti

- Un elemento a la vez, en orden de prioridad, en su propia rama `backlog/B##-<slug>` que sale de `dev`.
- Cada elemento termina con sus pruebas pasando y un commit. Se fusiona en `dev` y se sube a `dev`; nunca a `master`.
- Si aparece una decisión que te corresponde, no se improvisa: se apunta en «Para ti» con opciones y recomendación, y se sigue con el siguiente elemento.
- No se toca nada fuera de este repositorio. Los proyectos de prueba se crean en carpetas temporales.
- Al terminar cada elemento se actualiza su estado aquí.

## Para ti

Decisiones y pruebas que esperan tu atención.

- **Identidad de tu estudio** para los entregables (B04-B06): nombre, logo, color de acento y datos de contacto. Mientras tanto se usa una inventada, Quilla Estudio Digital (`templates/deliverables/`); la tuya irá en `~/.factory/studio/`.
- **Revisar el documento funcional de ejemplo** (B04).

## Elementos

| # | Elemento | Origen | Quién | Prioridad | Estado |
|---|---|---|---|---|---|
| B01 | Pruebas automáticas del comando `factory` | — | Sin ti | Alta | Pendiente |
| B02 | Revisión cruzada de especificaciones antes de aprobar | Nota 13 | Sin ti | Alta | Pendiente |
| B03 | Modo orquestador por proyecto, opcional | Nota 29 | Sin ti | Media | Pendiente |
| B04 | Entregable: documento funcional (PDF) | Nota 24, 2026-10-18 | Sin ti → revisas tú | Alta | Hecho; pendiente de tu revisión |
| B05 | Entregable: documento de diseño (PDF) | 2026-10-18 | Sin ti → revisas tú | Alta | Pendiente |
| B06 | Entregable: maqueta interactiva (ZIP) | 2026-10-18 | Sin ti | Alta | Pendiente |
| B13 | Página de ejemplo del kit de diseño «en acción» | Nota 5 | Sin ti | Baja | Pendiente |
| B14 | Paralelizar paquetes de tareas con worktrees transparentes: estudio y propuesta | Nota 14 | Sin ti → decides tú | Media | Pendiente |
| B07 | Definir la interfaz de stack (`docs/stack-interface.md`) | Modelo §13, nota 7, 2026-10-19 | Contigo | Alta | Pendiente |
| B16 | La plataforma lee el stack: `factory init --stack`, `factory stack list/show`, perfil con `stack` | B07 | Sin ti | Alta | Pendiente (tras B07) |
| B17 | Los agentes reciben las instrucciones del stack por rol | B07 | Sin ti | Alta | Pendiente (tras B16) |
| B18 | El panel y el enrutado obedecen al stack (vista previa, diseño, tokens) | B07, B15 | Sin ti | Media | Pendiente (tras B16) |
| B19 | Primer paquete: `web-static` | B07 | Sin ti → revisas tú | Alta | Pendiente (tras B16) |
| B20 | Paquete sin interfaz para comprobar el núcleo | B07 | Sin ti | Media | Pendiente (tras B16) |
| B21 | Despliegue según el stack, con aprobación humana | Nota 17, B07 | Contigo (definir) → sin ti | Media | Aparcado hasta B19 |
| B15 | Desacoplar el núcleo del stack web | Revisión 2026-10-19 | Sin ti | Alta | Pendiente |
| B08 | Retomar una sesión interrumpida | Corrección 5, nota 3 | Contigo (prueba real) | Alta | Pendiente |
| B09 | Prueba real del flujo completo con Boadilla Motor, incluido el diseño por hito | Notas 28 y 30 | Contigo | Alta | Pendiente |
| B10 | Fase de demo | Nota 16 | Contigo (definir) | Baja | Aparcado |
| B11 | Fase de entrega a producción | Nota 17 | Contigo (definir) | Baja | Incluida en B21 |
| B12 | Backend de estado en GitHub Projects | Modelo §13 | Contigo (decidir si merece la pena) | Baja | Aparcado |

## Detalle

**B01 · Pruebas automáticas del comando `factory`.** Hoy no hay ninguna; todo se ha probado a mano. Pruebas con `unittest` (sin dependencias) que creen proyectos temporales y recorran el enrutado de `factory next` por los dos carriles, la cola y la construcción automática, las acciones del panel (`apply_panel_action`), `move`, `remove`, `sync` con ramas locales y `design-import`. *Hecho cuando* `python3 -m unittest` pasa y cubre cada fila de la tabla de enrutado de `docs/state.md`. Va primero porque protege todo lo demás.

**B02 · Revisión cruzada de especificaciones.** Antes de presentarte una especificación, otro agente la cuestiona: incoherencias con otras especificaciones del hito, con la arquitectura base o con decisiones registradas, criterios no comprobables y huecos. Propuesta: el validador en un modo nuevo `spec_review` que escribe `spec-review.md`; si encuentra problemas, vuelve al analista una vez antes de llegarte. En el panel se ve junto a la especificación. *Hecho cuando* el enrutado lo incluye, está probado en B01 y documentado.

**B03 · Modo orquestador por proyecto.** `factory mode orchestrator on|off` crea o quita `.claude/settings.local.json` con `{"agent": "factory:orchestrator"}`, para que un `claude` normal en esa carpeta arranque como orquestador. Respeta lo que ya hubiera en ese fichero. `factory init` lo ofrece como opción. *Hecho cuando* activar y desactivar deja el fichero como estaba y está documentado en `docs/usage.md`.

### Entregables para el cliente (decididos el 2026-10-18)

Tres entregables, cada uno ligado a una aprobación del cliente. Todos con la **identidad de tu estudio** (fija en todos los proyectos, configurable una vez para toda la plataforma) y el logo del cliente en portada. Formales, sobrios y elegantes: tipografía de libro para títulos, sans legible para el texto, un solo color de acento, apartados numerados, pie con versión y página. Se generan como HTML con estilos de impresión y Chrome sin interfaz los pasa a PDF. Se guardan versionados en `.factory/deliverables/` y se descargan desde la vista Producto.

**B04 · Documento funcional.** Un único documento con **todo el roadmap**: detalle de los hitos ya definidos y resumen de los demás; nueva versión con cada hito definido. Sale cuando se aprueban todas las especificaciones de un hito. Contenido: portada (cliente, proyecto, versión, fecha, estado «Borrador para aprobación» / «Aprobado»), control de versiones, índice, introducción (objetivo, alcance y **fuera de alcance**), visión, roadmap (hitos con su objetivo y funcionalidades, sin fechas), funcionalidades por hito (descripción, para quién, criterios de aceptación redactados en frases con su ID), supuestos y dependencias, **pendiente del cliente** (datos, textos, imágenes), glosario y página de aprobación (nombre, fecha, firma). *Hecho cuando* `factory deliverable functional` genera el PDF de un proyecto de prueba, el panel lo ofrece y lo revisas tú.

**B05 · Documento de diseño.** Especificación de diseño con pantallas anotadas, como entregan las agencias al cliente: **un documento por hito con una sección autónoma por funcionalidad**. Sale cuando se aprueba el diseño del hito. Contenido: identidad visual al principio (principios, paleta, tipografía, logo, componentes base); por funcionalidad, objetivo con referencia al documento funcional, capturas de escritorio y móvil, anotaciones numeradas sobre la captura con su nota, estados (vacío, error, cargando, éxito), contenido que aporta el cliente, accesibilidad y qué criterios cubre cada pantalla; al final, cómo abrir la maqueta interactiva y los tokens como anexo. Las capturas salen de las maquetas con Chrome sin interfaz; las anotaciones, de marcas en la maqueta (`data-note`) junto a los IDs de criterio. *Hecho cuando* genera el PDF del hito de prueba y lo revisas tú.

**B06 · Maqueta interactiva.** Un solo prototipo navegable del hito (o de todo lo diseñado hasta ahora): las maquetas de las funcionalidades enlazadas con la navegación real, con portada e índice de pantallas, y entregado como **ZIP** que se abre con doble clic, sin publicar nada. Va con el documento de diseño. *Hecho cuando* `factory deliverable prototype` genera el ZIP y funciona abierto en local en escritorio y en móvil.

### Resto

**B13 · Kit «en acción».** Una página de ejemplo dentro de la galería del kit (portada, tarjeta, formulario) pintada solo con los tokens, para ver el kit aplicado y no solo sus muestras. *Hecho cuando* la galería la muestra con cualquier `tokens.json` válido.

**B14 · Paquetes en paralelo.** Estudiar si varios desarrolladores pueden trabajar a la vez con worktrees que el humano nunca ve (creados y borrados por la plataforma, fuera de la carpeta del proyecto), cómo afecta a la guardia, a la vista previa y a los conflictos entre ramas. Sale un documento con la propuesta y sus riesgos; **la implementación espera a tu decisión**.

### Conexión con el stack

El contrato está en `docs/stack-interface.md`: qué declara un stack (identidad y requisitos, interfaz, diseño, estructura y comandos, pruebas, vista previa, entornos y despliegue, entregables e instrucciones por rol) y cómo lo lee la plataforma.

**B07 · Definir la interfaz de stack.** Revisar contigo `docs/stack-interface.md` y cerrar sus preguntas: formato, primeros stacks, en qué momento se elige, dónde viven los stacks propios y hasta dónde llega el despliegue automático. *Hecho cuando* el documento no tiene preguntas abiertas.

**B16 · La plataforma lee el stack.** Carpeta `stacks/` (y `~/.factory/stacks/`), `factory stack list` y `factory stack show`, `factory init --stack <id>` que verifica los requisitos de la máquina y fija `stack` y `stack_version` en el perfil, comandos del perfil sembrados desde el stack, y el orquestador preguntando el stack en el arranque o proponiéndolo en el descubrimiento. Sin stack, todo como hoy. *Hecho cuando* está probado en B01.

**B17 · Instrucciones del stack por rol.** Cada agente lee `stacks/<id>/agents/<rol>.md` al empezar, como hoy `shared/agent-rules.md`; el arquitecto parte de la arquitectura de referencia y las transversales tipo del stack en vez de improvisarlas. *Hecho cuando* un proyecto con stack lleva sus instrucciones a los seis roles.

**B18 · Panel y enrutado según el stack.** La pestaña de vista previa sale solo si el stack la declara (estática o servidor); el paso de diseño, los tamaños de pantalla, la tarea de tokens y la comprobación del validador salen del stack. Incluye los puntos 1-3 de B15.

**B19 · Paquete `web-static`.** El primero: web estática como Boadilla Motor (estructura, comandos, pruebas en navegador sin interfaz, accesibilidad, tokens a CSS, vista previa estática, publicación en GitHub Pages, plugin `frontend-design`). Lo revisas antes de darlo por bueno.

**B20 · Paquete sin interfaz.** Uno mínimo (p. ej. una librería o un proceso en Python) para comprobar que el flujo completo funciona sin pantallas ni pasos de web.

**B21 · Despliegue según el stack.** Entornos, cómo se despliega a cada uno, credenciales siempre del humano, qué aprobación exige cada despliegue y cómo se revierte. Sustituye a la nota 17 y cambia la regla «ningún agente despliega» por la que se decida. Se define contigo tras B19.

**B15 · Desacoplar el núcleo del stack web** (revisión del 2026-10-19). El núcleo (estado, carriles, enrutado, ramas y PRs, guardia, TDD con los comandos del perfil, analista, validador, documento funcional) ya es independiente del stack. Lo que está atado a la web sin necesidad:
1. **`interface: web|none|mixed`** mezcla «tiene pantallas» con «es web». Pasar a `ui|none|mixed` (aceptando `web` en proyectos antiguos); el tipo de interfaz (web, app móvil, escritorio, Salesforce…) lo dice el stack.
2. **Vista previa**: supone ficheros estáticos con `index.html` (`preview_root`, `preview_url`). Debe declararla el stack (`static`, `url` o ninguna) y el panel ocultar la pestaña si no hay.
3. **Tokens de diseño en código**: el arquitecto crea siempre la tarea «Implementar los tokens» pensando en CSS y el validador comprueba «sin colores escritos a mano». Debe ser «como indique el stack» (CSS, tema de la app, SLDS…).
4. **Textos con la web por defecto**: GitHub Pages en la pregunta del repositorio, «recomendado para webs» en el nivel de diseño, ejemplos del descubrimiento solo web, `frontend-design` recomendado para cualquier interfaz. Redactarlos en neutro o moverlos al paquete web.
5. **Se queda como está, a propósito**: las maquetas y el lienzo son HTML porque son el medio para enseñar y aprobar pantallas, sea cual sea el stack final (son desechables); el kit de diseño en `tokens.json` es un formato neutro (W3C).
*Hecho cuando* un proyecto de prueba con una interfaz no web y otro sin interfaz recorren el flujo sin textos ni pasos de web.

**B08 · Retomar una sesión.** Cerrar la sesión con una decisión pendiente y con un agente trabajando, volver a abrirla y comprobar qué ve el orquestador y qué hace. Hace falta una sesión real; sin ti solo se puede preparar el guion de prueba.

**B09 · Prueba real completa.** Boadilla Motor desde cero con el flujo actual, hasta al menos el primer hito construido. Saldrán notas nuevas.

**B10-B12.** Aparcados hasta que los definamos juntos.
