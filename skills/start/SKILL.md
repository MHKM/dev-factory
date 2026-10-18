---
name: start
description: Arranca o retoma un proyecto de factory. Úsala como primer mensaje de la sesión del orquestador (la lanza `factory-start`) o cuando el humano pida volver a ver el estado.
---

Sigue tu **protocolo de arranque** (sección «Protocolo de arranque» de tus instrucciones de orquestador):

1. Si no existe `.factory/project.md`, saluda en una línea y pregunta qué quiere construir.
2. Si existe, ejecuta `factory sync` y `factory next` y resume el estado en 3-5 líneas.
3. Asegúrate de que el panel está en marcha y da su URL.

No repitas estas instrucciones al humano: actúa.
