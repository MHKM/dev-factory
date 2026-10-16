# Notas de la demo · Boadilla Motor Sport

Observaciones durante la primera ejecución real de la plataforma (2026-10-14). Pendientes de revisar después de la demo.

| # | Nota |
|---|---|
| 1 | Panel, «Trabajando ahora»: aparece «project · Proyecto» y no se ve qué rol está trabajando (era el arquitecto; solo lo dice la terminal). |
| 2 | El panel mezcla español e inglés. La interfaz debe estar entera en un idioma, a elegir (español o inglés), sin mezclas raras. Los entregables (código) siempre en inglés. |
| 3 | Retomar tras cerrar la sesión con una decisión pendiente: ¿se retoma bien?, ¿qué contexto necesita el orquestador? Probarlo y discutirlo. |
| 4 | Había dos agentes trabajando a la vez (prototipador y arquitecto), pero el panel solo mostraba una línea «project · Proyecto». El panel debe mostrar cada agente activo, con su rol y lo que hace. (Observación mía para revisar: los dos trabajaban sobre el mismo elemento `project`, que solo tiene una situación, y el enrutado los preveía en secuencia, no en paralelo.) |
| 5 | Kit de diseño: cuesta ver el resultado. Incluir componentes o un ejemplo en HTML que muestre los colores, la tipografía, etc. aplicados «en acción». (Observación mía: la galería ya tiene componentes al final; quizá falta una página de ejemplo realista o que se vean antes.) |
| 6 | Un agente estaba rehaciendo el diseño y el panel no mostraba que estuviera trabajando. Importante: siempre que haya agentes trabajando, el panel tiene que mostrarlo. (Observación mía: hoy el panel solo sabe que alguien trabaja si el agente marca `in_progress` en el estado; si no lo hace, o el orquestador lo lanza sin pasar por ahí, es invisible.) |
| 7 | Calidad visual del diseño y las maquetas: funcionales pero con aspecto genérico («muy Claude Code»). Para web hará falta algo más creativo y bonito. No es un fallo de la plataforma: es trabajo pendiente del stack web. Para probar el orquestador y la herramienta en general, vale como está. |
| 8 | Poder aprobar (diseños y demás puntos de decisión) desde el propio panel, sin tener que contestar al orquestador cada vez. Estudiar si es posible. |
| 9 | Las tareas transversales que arrancaron los desarrolladores al principio parecen quedarse en «Desarrollo» para siempre: se siguen aprobando diseños y no cambian de estado. **Actualización:** al final cambiaron; parece que solo tardaban. Queda como nota: el panel no deja claro si una tarea larga sigue avanzando o está atascada. |
| 10 | Integrar la terminal (la conversación con el orquestador) en la vista Construcción, con el input ahí cuando se necesite información (sobre un diseño, etc.). Junto con los botones de aprobar y pedir cambios (nota 8). Estudiar si es posible. |
| 11 | En algún momento debería abrirse el navegador con la web que se está construyendo, para verla avanzar en directo (vista previa de la release o de la rama en curso). |
| 12 | Un diálogo con el orquestador en la parte inferior del panel, estilo terminal pero menos verboso: que vaya diciendo «tienes que aprobar esto y esto», que se pueda hablar con él desde ahí (es la sesión principal) y aprobar desde el propio panel. Amplía las notas 8 y 10. Estudiar si es posible. |
| 13 | El arquitecto detectó tarde una decisión importante (barra fija frente a la de la maqueta en móvil) que contradecía la maqueta ya aprobada. Añadir en la fase de especificación una validación por otro agente que cuestione la especificación y la maqueta y detecte incongruencias al principio, antes de aprobar. |
| 14 | Los paquetes de tareas se ejecutan en secuencia (ahora hay dos esperando). Estudiar cómo paralelizarlos, por ejemplo con worktrees, pero de forma **transparente**: el usuario no debe notar que existen ni tener que gestionarlos, y no deben crear conflictos en el repositorio. (Revisa la decisión de «sin worktrees», que se tomó porque son difíciles de gestionar para un humano.) |
| 15 | «Trabajando ahora» (insiste en las notas 1, 4 y 6): mostrar cada agente identificado y, bajo él, las tareas que está haciendo (hoy salen como tareas sueltas). Pedirá una propuesta de diseño de esta parte para validarla antes de construirla. |
| 16 | Fase de **demo**: al terminar la web, entregar una demo de ella. Idea: un paseo por la web mostrando cosas (formato por definir). |
| 17 | Fase de **entrega**: poner la web en producción con la configuración del stack elegido. La forma de entregar depende del nivel y tipo de stack. (Choca con la regla actual «ningún agente despliega»: habrá que definir con qué aprobación humana se permite.) |
| 18 | Al aprobar una PR, poder ver funcionando lo que se ha construido en esa rama (vista previa) para pedir cambios en ese momento si hace falta. Relacionada con la nota 11. |
| 19 | Alerta sonora cuando una fase termine y requiera la atención del humano (algo pasa a «Te espera»). |
| 20 | Enlace directo a la PR para aprobarla (en el panel y en lo que presenta el orquestador). (Observación mía: el panel ya enlaza «PR #n» en las tarjetas si el repo es de GitHub; revisar por qué no se ve o no basta.) |
| 21 | En la validación final (lote) no se abre el navegador. Al llegar a ese paso, la web debería estar ya abierta o lanzarse un visor especial para verla en varios formatos (móvil y escritorio); valorar si se puede lanzar Chrome con esa configuración por defecto. Estudiar si es posible. |
| 22 | Tercera pestaña (o botón) en el panel para ver la web construida, o al menos su estado actual, con botón de refrescar. Relacionada con las notas 11, 18 y 21. |
| 23 | Resultado final muy limitado en diseño (confirma la nota 7). Mejorar la fase de diseño: una maqueta funcional con un diseño bien hecho, probablemente liderada por el lienzo de diseño de claude.ai (tipo «Design»), en lugar del HTML que genera hoy el prototipador. |

## Estado (2026-10-16)

| Bloque | Notas | Estado |
|---|---|---|
| Corrección 1 · Visibilidad de los agentes | 1, 6, 15 | ✅ Hook de actividad (inicio, fin, última acción por agente) y «Trabajando ahora» con una tarjeta por agente. Avisa si un agente lleva más de 5 min sin actividad (cubre en parte la 9). |
| Corrección 2 · Dos agentes sobre el proyecto | 4 | ✅ El kit de diseño es un elemento propio (`design`); arquitectura base y diseño avanzan en paralelo sin pisarse. |
| Corrección 3 · Idioma | 2 | ✅ Un único idioma (`language`) para panel, mensajes del comando, guardia, documentos y conversación; el código siempre en inglés. |
| Corrección 4 · Enlace a la PR | 20 | ✅ Botón «Abrir PR» en «Te espera», en el hito y en la ficha lateral. |
| Corrección 5 · Retomar la sesión | 3 | Pendiente de probar. |
| Mejoras | resto | Pendientes (ver la clasificación acordada). |
