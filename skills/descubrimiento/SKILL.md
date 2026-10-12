---
name: descubrimiento
description: Modo descubrimiento del orquestador de factory. Conversa con el humano para entender y definir lo que quiere construir, propone ideas, prioriza y produce la visión, el roadmap por hitos y las funcionalidades. Úsala al empezar un proyecto, ante peticiones poco definidas y para revisar el roadmap al cerrar un hito.
---

# Descubrimiento

Conversas directamente con el humano para **descubrir y definir** lo que quiere, no solo para tomar nota. Es la única fase en la que se habla con él de forma abierta.

Las plantillas están en `${CLAUDE_PLUGIN_ROOT}/plantillas/` (`vision.md`, `roadmap.md`).

## Cómo conversar

- **Pocas preguntas por ronda**: 3 o 4 como mucho, empezando por lo que más cambia el resultado.
- Las preguntas cerradas van con `AskUserQuestion`: opciones concretas y la recomendada primero. Las abiertas («cuéntame cómo trabaja ahora…») van en el chat.
- **Propón ideas que no ha pedido** cuando aporten valor claro, marcadas como `💡 Sugerencia`, cada una con su beneficio en una línea. El humano decide si entran.
- **No preguntes por tecnología.** El stack lo propone el arquitecto en la arquitectura base, con su propia consulta. Si el humano expresa una preferencia o una restricción técnica (hosting que ya tiene, dominio, herramientas), anótala como restricción.
- Si algo no se puede cerrar ahora, apúntalo en «Preguntas abiertas» y sigue.
- Resume lo entendido antes de escribir nada, para que el humano lo corrija.

## Rondas (modo inicial)

1. **Entender.** Qué quiere conseguir, para quién y por qué ahora. Cómo se resuelve hoy. Ejemplos o referencias que le gusten.
2. **Explorar.** Qué tiene que poder hacer cada tipo de usuario. Aquí entran tus sugerencias. Pregunta por lo que suele olvidarse en ese tipo de producto.
3. **Priorizar.** Clasifica cada funcionalidad junto con el humano como `imprescindible`, `deseable` o `más adelante`.
4. **Contexto y restricciones.** Contenidos que aporta él (textos, fotos, logo), cuentas o servicios que ya tiene, plazos, presupuesto, quién mantiene luego el sistema, idiomas, requisitos legales (p. ej. aviso de privacidad si se recogen datos personales).
5. **Roadmap.** Propón hitos:
   - El primero, pequeño y usable de principio a fin.
   - Cada hito con su «al terminar se puede…».
   - En un proyecto pequeño, un solo hito está bien.

### Ejemplo de primeras preguntas

Para «una web para el taller de mi primo en Boadilla, con los servicios y un formulario para que le llamen para cita»:

- ¿Qué servicios ofrece y quiere mostrar precios o solo la descripción?
- Cuando alguien rellena el formulario, ¿cómo quiere enterarse: email, WhatsApp, ambos?
- ¿Tiene ya dominio, logo o fotos del taller?
- 💡 Sugerencias: ubicación con mapa y horario; botón de llamada y de WhatsApp en móvil; ficha de Google Business enlazada; aviso de privacidad y consentimiento en el formulario (obligatorio si recoge datos personales).

## Al terminar

1. Escribe `.factory/artefactos/vision.md` y `.factory/artefactos/roadmap.md` con las plantillas.
2. Crea los elementos:
   - Hitos: `factory nuevo hito --titulo "…" --objetivo "<al terminar se puede…>"`.
   - Funcionalidades de **cada** hito, con su descripción en lenguaje de negocio:
     ```
     factory nuevo func --titulo "…" --hito H01 --prioridad imprescindible --texto - <<'EOF'
     <qué necesita el usuario, qué tiene que poder hacer, datos y detalles hablados, sugerencias aceptadas que incluye>
     EOF
     ```
     Las que quedaron como «más adelante» van solo en `roadmap.md`, sin elemento.
   - `--depende` si una funcionalidad necesita otra.
3. Marca el perfil: `factory set proyecto descubrimiento=hecho interfaz=<web|ninguna|mixta> descripcion="<una línea>"`.
4. Registra como decisión lo que se haya decidido de forma explícita (prioridades, ideas descartadas y su motivo): `factory decision --titulo "Alcance inicial" --ref proyecto --texto -`.
5. Cuéntale al humano en 3-4 líneas qué queda definido y que el siguiente paso es la arquitectura base. Vuelve al bucle del orquestador.

## Modo revisión (al cerrar un hito o ante una petición nueva)

1. Lee `vision.md`, `roadmap.md`, el `lote.md` del hito cerrado y las decisiones recientes.
2. Pregunta solo lo necesario: qué ha aprendido con lo entregado, qué cambia de prioridad y qué es nuevo.
3. Actualiza `roadmap.md` (y `vision.md` si cambia el alcance). Crea los nuevos hitos y funcionalidades, y aplaza o descarta lo que ya no aplica.
4. Para una petición nueva a mitad de un hito, decide con el humano si entra en el hito actual o en uno posterior.
