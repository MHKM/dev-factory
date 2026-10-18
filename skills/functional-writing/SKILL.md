---
name: functional-writing
description: Cómo escribir en factory los textos que acaban en el documento funcional del cliente (vision.md y las especificaciones spec.md) para que siempre salga igual de claro y formal. Úsala al escribir o revisar la visión o una especificación, y antes de generar el documento funcional.
---

# Escribir para el documento funcional

El documento funcional que recibe el cliente (`factory deliverable functional`) se monta solo a partir de `vision.md` y de cada `spec.md`. La maqueta del documento es fija; **lo que lo hace bueno o malo es el texto**. Estas reglas son para que todos los proyectos se lean igual: claros, formales y sin tecnicismos.

## Para quién escribes

Para el cliente, que no es técnico y va a firmar el documento. Cada frase tiene que poder leerla el dueño del negocio y entender qué va a tener y qué no.

- Escribe en el idioma del proyecto (`language` en `.factory/project.md`), en tono formal y cercano: frases cortas, voz activa, presente.
- Habla de lo que ve y hace el usuario, nunca de cómo se construye. Prohibido: API, backend, frontend, base de datos, servidor, componente, endpoint, JSON, HTML, CSS, etiquetas como `h1`, nombres de librerías o de ficheros, y cualquier texto entre comillas invertidas.
- Usa siempre los mismos nombres para lo mismo: si en la visión es «solicitud de cita», no pases a «reserva» en otra especificación. Si un término puede no entenderse, añádelo al glosario.
- Nada de adjetivos sin contenido («moderno», «intuitivo», «rápido», «potente»).
- Es un documento de **producto**, no de seguimiento: nada sobre el estado del trabajo (aprobado, pendiente de especificar, en construcción, aplazado, tareas, versiones internas). El generador tampoco lo muestra; no lo metas en el texto.

## Datos que no sabemos

Nunca inventes datos del negocio (teléfonos, direcciones, precios, horarios, razón social, plazos). Márcalos siempre así, y solo así:

`[pendiente: <qué falta, en minúsculas>]`, por ejemplo `[pendiente: horario por días]`.

El documento los recoge todos en «Pendiente del cliente», con dónde se usan. Otras formas (`[TELÉFONO]`, `XX`, «TBD», «por definir») no se recogen y el generador avisa.

## `vision.md`

Respeta los títulos de la plantilla, porque el documento los busca por su nombre:

| Sección | Qué poner | En el documento |
|---|---|---|
| `## Objetivo` | 2-3 frases: quién es el cliente, qué problema resuelve el producto y para quién | 1.1 Objetivo, en grande |
| `## Destinatarios` | Lista `- **Perfil**: qué necesita y cómo lo usará` | 1.2 Destinatarios |
| `## Alcance` | Dos líneas: `**Dentro:** …` y `**Fuera:** …`. Lo de fuera, explícito: evita discusiones con el cliente | 1.3 Alcance |
| `## Restricciones y datos de contexto` | Lista de hechos que condicionan el producto | Supuestos y dependencias |
| `## Glosario` | Lista `- **Término**: definición en una frase` | Glosario |
| `## Preguntas abiertas` | Lista de lo que falta decidir, con `[pendiente: …]` si es un dato | Pendiente del cliente |

Las secciones internas (funcionalidades, ideas propuestas) no salen en el documento.

## `spec.md`

Títulos exactos de la plantilla (`${CLAUDE_PLUGIN_ROOT}/templates/spec.md`):

- **`## Necesidad`**: una o dos frases desde el punto de vista de quien lo usa: qué quiere conseguir y por qué. Sale destacada.
- **`## Comportamiento`**: un párrafo con el flujo principal y los alternativos, como se lo contarías al cliente.
- **`## Criterios de aceptación`**: cada criterio en una línea con esta forma exacta, porque el documento la parte en tres columnas (situación, acción, resultado):

  `- **AC-F###-NN** — Dado <situación>, cuando <acción>, entonces <resultado observable>.`

  - Primera persona del usuario («Dado que estoy en…», «cuando pulso…», «entonces veo…»).
  - La situación es el punto de partida, la acción es una sola cosa que hace el usuario, y el resultado es algo que se ve o se puede comprobar.
  - Incluye los casos de error y los límites (campo vacío, formato no válido, falta de conexión).
  - Si no hay acción, puedes omitir «cuando», pero mejor no.
- **`## Datos`**: tabla `| Dato | Obligatorio | Reglas |` con reglas comprensibles («número español de 9 cifras», no expresiones regulares).
- **`## Fuera de alcance`**: lista de lo que esta funcionalidad no hace, y si lo hace otra, cuál.
- **`## Supuestos y preguntas resueltas`**: lo que se ha dado por hecho, con la decisión (`D###`) si se preguntó.

## Antes de dar por buena la visión o una especificación

Ejecuta `factory deliverable functional --check`: revisa la visión y todas las especificaciones sin generar ninguna versión, y lista lo que no cumple estas reglas (criterios que no siguen la forma, secciones que faltan, tecnicismos, datos pendientes mal marcados). Corrígelo en el origen hasta que no salga ningún aviso. El documento nunca se edita a mano: se corrige el origen y se vuelve a generar.
