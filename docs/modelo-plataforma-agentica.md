# Suite de Desarrollo Agéntico — Modelo de diseño

> Documento de contexto para Claude Code. Recoge las decisiones de diseño acordadas hasta ahora.
> **Estado: fase de diseño.** Nada de esto está implementado todavía. Las decisiones son revisables: si el proceso resulta demasiado complejo, se simplificará.
> Este repositorio (`dev-factory`) contiene **la plataforma** (modelo, agentes, skills). Cada construcción real que se haga con ella vive en **su propio repositorio**.

---

## 1. Visión

Una plataforma multiagente para construir software donde:

- Un **orquestador conversacional** es el único interlocutor del humano y lanza agentes especializados según haga falta.
- Cada agente tiene un **rol** concreto (descubrimiento, análisis, arquitectura, desarrollo, validación…) y un **modelo elegible** por agente.
- El humano **supervisa** el estado del trabajo con una vista sencilla tipo kanban y solo interviene en puntos de decisión concretos.
- No hace falta pedirlo todo de forma exacta: la plataforma ayuda a **descubrir y definir** la necesidad (brainstorming), no solo a ejecutarla.

### Principios

1. **Simplicidad ante todo.** Ante la duda, la opción con menos piezas.
2. **Multitecnología.** La tecnología de cada proyecto se elige e indica en su contexto. Los agentes son genéricos por rol; el conocimiento de cada stack se inyecta como pieza enchufable.
3. **Desacoplamiento del almacenamiento.** Las tareas, sus estados y el diseño de la plataforma no dependen del sistema que los almacene. Se accede siempre a través de una capa propia. Primer backend: ficheros `.md` locales (§10); más adelante, GitHub Projects u otro consumible por API.
4. **Un solo usuario.** Cada proyecto lo gestiona una persona. En el futuro se podrá exponer el estado y las tareas a otros, pero no se diseña para concurrencia.
5. **El humano decide en los puntos clave, y solo en ellos.** Evitar saturarle.
6. **Preguntar antes de actuar.** Ante una decisión relevante, un agente pregunta con opciones y recomendación en lugar de inventar.

---

## 2. Jerarquía del trabajo

```
Proyecto
 └── Hito (etapa del roadmap; a veces solo hay uno)
      ├── Funcionalidad
      │    ├── Artefactos funcionales (spec, criterios de aceptación, maqueta / reglas de negocio)
      │    └── Tareas técnicas
      └── Tareas transversales (core de plataforma)
```

- **Hito**: etapa del roadmap de construcción. Tiene un objetivo y algo usable al final ("al terminar, se puede hacer X").
  - Se usa "hito" para el roadmap y "fase" para el ciclo de vida, para no confundirlos.
- **Funcionalidad**: necesidad de negocio. Cuelga de un hito.
- **Artefacto funcional**: describe *qué* se quiere. No se "trabaja": se redacta, se aprueba y queda como referencia. No es una tarea.
- **Tarea**: unidad de trabajo asignable, con estado, que termina. Puede ser:
  - **Técnica**: cuelga de una funcionalidad.
  - **Transversal / core**: cuelga directamente del hito (ver §6).

---

## 3. Flujo general

```
Descubrimiento → Visión + Roadmap + Arquitectura base (aprobados)
   → por cada hito aprobado (se abre su rama release, §12):
       Análisis funcional → Maqueta / reglas de negocio (aprobadas)
       → Diseño técnico con interfaces (con consulta previa si hace falta)
       → Tests → Implementación → Validación
       → Aceptación en lote (= fusión de la release a la rama principal)
   → al cerrar el hito: revisión del roadmap
```

- El roadmap completo sale del descubrimiento **a alto nivel**.
- La especificación funcional y el diseño técnico detallados se hacen **solo para el hito que se aprueba**, no antes (lo lejano cambiará).
- Al cerrar cada hito, el orquestador puede volver a invocar al agente de descubrimiento para ajustar los siguientes.

---

## 4. Agentes

| Agente | Responsabilidad | Entrega |
|---|---|---|
| **Orquestador** | Único interlocutor del humano. Mantiene la visión global, lanza agentes, presenta lo que requiere atención. No hace el trabajo él mismo. | — |
| **Descubrimiento** | Agente de alta capacidad. Escucha la necesidad, pregunta y **propone ideas no pedidas** (marcadas como sugerencias). Prioriza con el humano (imprescindible / deseable / más adelante). | Visión, roadmap por hitos |
| **Arquitecto** | Arquitectura base al inicio. Por hito: diseño técnico (incluidas las **interfaces** que permiten escribir los tests), tareas técnicas y transversales, paquetes de trabajo. Decide si hace falta consulta previa. | Arquitectura base, diseño técnico, tareas |
| **Analista** | Baja cada funcionalidad del hito a especificación con criterios de aceptación. | Especificación funcional |
| **Prototipador** | Genera la maqueta HTML navegable (solo desarrollos web). | Maqueta |
| **Desarrollador** | Escribe **primero los tests** (a partir de los criterios de aceptación y las interfaces del diseño) y después implementa hasta que pasan. Trabaja en su rama. | Tests + código + pull request |
| **Validador** | Comprueba que lo construido cumple los criterios. Debe ser independiente (otro modelo o sin acceso al razonamiento del desarrollador). | Informe de validación |

No hay agente tester: los tests los escribe el desarrollador antes de implementar (§5, Tarea).

### Reglas de interacción

- **Los agentes no hablan directamente con humanos.** Si necesitan algo, la tarea pasa a *Esperando humano* y el orquestador lo presenta.
- **Excepción: el agente de descubrimiento**, que conversa directamente con el humano porque es un diálogo de ida y vuelta. Puede invocarse al inicio del proyecto y también más adelante ante peticiones poco definidas.
- Las preguntas se plantean **con opciones y recomendación** ("A o B, recomiendo A por esto").
- Las respuestas del humano se guardan en el **registro de decisiones**.

### Granularidad

- **Unidad de seguimiento**: la tarea unitaria (para ver progreso, validar y reintentar solo lo que falla).
- **Unidad de asignación**: el **paquete**, un grupo de tareas cohesionadas que hace un mismo agente seguidas, con todo el contexto. Lo propone el arquitecto (mismo componente, dependencias, contexto compartido).
- En proyectos pequeños, un solo agente puede hacerlo todo.
- Lo común o lo que se pisaría va en el mismo paquete.
- Un buen diseño técnico reduce la necesidad de contexto compartido.

---

## 5. Ciclo de vida

Se separan dos dimensiones:

- **Fase**: en qué punto del ciclo está.
- **Situación** (común a todos los niveles): *En cola*, *En curso*, *Esperando humano*, *Bloqueada*.

✋ = punto de decisión humana.

### Ciclo del esqueleto (acordado)

Para la primera versión se usa un ciclo **reducido**. Mantiene los mismos puntos de decisión humana que el modelo completo y solo quita fases intermedias. Se ampliará cuando haga falta distinguirlas.

```
Hito:           Propuesto → ✋ Aprobado → Cerrado
Funcionalidad:  Definida → ✋ Especificada → En construcción → Validada → ✋ Aceptada
Tarea:          Pendiente → En curso → ✋ En revisión → Hecha
```

- **Funcionalidad**
  - *Especificada* ✋: el humano aprueba la especificación y la maqueta o las reglas de negocio. Si la rechaza, vuelve a *Definida* con comentarios.
  - *En construcción* incluye el diseño técnico (con su consulta previa, que se expresa con la situación *Esperando humano*) y las tareas.
  - *Validada*: el validador ha comprobado los criterios; espera al lote.
  - *Aceptada* ✋: aceptada en el lote del hito.
  - Salidas laterales: **Aplazada** (a un hito posterior) y **Descartada**.
- **Tarea**
  - *En curso*: el desarrollador escribe los tests, **los commitea antes que la implementación** (así un cambio posterior en ellos queda visible en la PR) y luego implementa hasta que pasan.
  - Si los tests no pasan tras N intentos → situación *Bloqueada*.
  - *En revisión* ✋: validador + PR; el humano aprueba la fusión a la rama release.

### Modelo completo (referencia para ampliar)

- Hito: Propuesto → ✋ Aprobado → En análisis → En construcción → ✋ Aceptado → Cerrado
- Funcionalidad: Definida → En análisis → ✋ Revisión funcional → En diseño técnico → En construcción → En validación → Pendiente de aceptación → ✋ Aceptada en lote → Terminada
- Tarea: Pendiente → Tests → Implementación → Revisión (validador + PR) → ✋ Fusión → Hecha

### Revisión técnica
- No hay revisión humana sistemática del diseño. Se sustituye por la **consulta previa** del arquitecto.
- Solo se pide intervención en elementos muy core o complejos, y el arquitecto **deja escrito el motivo**.
- Criterios orientativos: cambios en arquitectura base o modelo de datos principal, seguridad/permisos, integraciones externas, rendimiento, decisiones difíciles de revertir, mucha incertidumbre.
- **Salvaguarda automática**: si el diseño contradice la arquitectura base o una decisión registrada, la consulta es obligatoria.
- Lo aprobado automáticamente sigue siendo visible y revisable.

### Aceptación en lote
- Las funcionalidades validadas esperan en *Validada* sin interrumpir.
- El orquestador presenta un **lote** al cerrar el hito, o antes si se acumulan o si otras dependen de ellas.
- Dentro del lote se acepta o rechaza **cada funcionalidad por separado**.
- El lote incluye resumen: qué contiene, cómo probarlo, qué ha comprobado el validador.
- **Rechazo** → se corrige **dentro de la misma release** con nuevas tareas y se vuelve a presentar. La release no se fusiona a la rama principal hasta que todo lo que contiene esté aceptado.
- **Aplazar o descartar** algo ya construido es la excepción: un agente prepara un revert explícito y el humano lo aprueba.

### Cambios
- Un cambio de requisito crea una nueva versión de la funcionalidad e invalida las tareas afectadas.

---

## 6. Tareas transversales (core de plataforma)

Tareas necesarias que no aportan funcionalidad de negocio (repositorio, entornos, CI, autenticación base, modelo de datos principal, componentes comunes; más adelante refactors, actualizaciones, deuda técnica).

- Cuelgan **del hito**, no de una funcionalidad.
- Las genera el **arquitecto** a partir de la arquitectura base.
- Se validan con **criterios técnicos** ("los tests se ejecutan en cada cambio", "el despliegue a pruebas funciona").
- Las funcionalidades **pueden depender** de ellas.
- Aparecen en el tablero, pero no en la vista funcional (o solo en un apartado "base técnica").
- Al inicio se concentran en el primer hito ("hito de cimientos").

---

## 7. Arquitectura base y memoria del proyecto

- **Arquitectura base ligera** al inicio, junto al roadmap: solo decisiones estructurales (stack, arquitectura, modelo de datos principal).
- Cada hito diseña dentro de ese marco. Cambiarlo requiere una decisión explícita.
- **Registro de decisiones** en `.factory/decisiones/` (qué se decidió y por qué). Los agentes lo consultan antes de actuar.
- Para proyectos existentes: fase de **reconocimiento** inicial que genera un mapa del proyecto.

---

## 8. Artefactos y espacio de trabajo `.factory/`

**El repositorio de la construcción solo versiona entregables** (código, tests, configuración). Todo lo demás vive en `.factory/`, una carpeta **local, en el `.gitignore` y sin versionar**:

```
<repo de la construcción>/
  src/ …              ← entregables: ramas y PRs (§12)
  .factory/           ← local, no versionado
    estado/           ← backend de ficheros: hitos, funcionalidades, tareas (§10)
    artefactos/       ← visión, roadmap, specs, maquetas, diseños, informes
    decisiones/       ← registro de decisiones
```

- Como `.factory/` está fuera de git, un cambio de rama no le afecta: los agentes que no programan escriben siempre en el mismo sitio, sea cual sea la rama activa.
- Las tareas del tablero solo **enlazan** a los artefactos (desacoplados del backend).
- En el futuro podrá decidirse commitear algunos artefactos aprobados (p. ej. en `docs/`) o compartirlos; de momento no.

| Fase | Artefacto |
|---|---|
| Descubrimiento | Visión (objetivo, destinatarios, alcance, ideas aceptadas y descartadas, preguntas abiertas), roadmap por hitos |
| Arquitectura | Arquitectura base, registro de decisiones |
| Análisis | Especificación con criterios de aceptación; maqueta HTML (web) o reglas de negocio |
| Diseño técnico | Diseño técnico con interfaces, tareas, paquetes |
| Implementación | Tests, código, pull request (en el repositorio) |
| Validación | Informe de validación |

### Maqueta y reglas de negocio
- **Desarrollos web**: maqueta HTML navegable para dar el ok antes de desarrollar.
  - Es **desechable**: valida el *qué*, no es base de código.
  - Los comentarios sobre la maqueta vuelven al analista.
- **Desarrollos sin interfaz** (backend Apex, triggers, integraciones): funcionalidades de negocio en lenguaje humano, agrupadas por área, con formato **"cuando ocurre X, el sistema hace Y"**.
- **Proyectos mixtos**: ambas cosas, colgando de la misma funcionalidad.

---

## 9. Multitecnología

- **Perfil de proyecto**: indica tecnología, versiones, convenciones y comandos. Se inyecta en el contexto de cada agente.
- **Paquetes de conocimiento por tecnología** (skills): buenas prácticas, patrones, errores típicos.
- **Adaptadores de herramientas**: interfaz común (`build`, `test`, `lint`, `deploy`) que cada stack implementa. Los agentes llaman a "ejecuta los tests" sin saber qué hay debajo.
- Stacks con entornos especiales (p. ej. Salesforce: scratch orgs / sandboxes) → el adaptador gestiona también esos entornos.
- Proyectos mixtos: el perfil admite varios componentes y cada tarea indica a cuál afecta.
- Recomendación: validar la abstracción empezando con dos stacks muy distintos.

---

## 10. Backend del tablero

Los agentes nunca leen ni editan el estado directamente: usan una **capa común** con operaciones como `crear`, `mover a fase`, `marcar esperando humano`, `listar pendientes`. Cambiar de backend solo cambia lo que hay debajo de esa capa.

### Primer backend: ficheros en `.factory/estado/`
- Un `.md` por elemento (hito, funcionalidad, tarea), con su estado en el frontmatter: fase, situación, agente, intentos, rama, PR, enlaces a artefactos.
- Legible por humanos y agentes; persiste entre sesiones (el orquestador reconstruye el estado al arrancar).

### Backend futuro: GitHub Projects
- Consumible por API (GraphQL).
- Las issues solo tienen abierto/cerrado; los estados reales van en el **campo Status** del Project.
- Recursos útiles: sub-issues (jerarquía), tipos de issue, dependencias, automatizaciones.
- **Agente asignado**: campo personalizado "Agente". El campo de asignados se reserva para personas.
- Sería la vía natural para exponer el estado a otras personas si algún día hace falta.

---

## 11. Vistas (HTML local, consume el backend)

De momento son **solo de consulta** y leen el backend a través de la misma capa. Actualización por consulta periódica.

1. **Requiere tu atención**: lo que está en *Esperando humano* o *Bloqueado*, con el motivo.
2. **Tablero por fase**: columnas por fase; en cada tarjeta, agente asignado y situación. La vista por agente es un filtro.
3. **Progreso del proyecto**: hitos → funcionalidades → tareas, con avance.
4. **Vista funcional**: la solución en lenguaje de negocio, basada en los artefactos de análisis (hitos → funcionalidades → maqueta o reglas de negocio).

---

## 12. Código y control

### Modelo de ramas (repos de construcción)

```
master ──────────────────────────────●─────────  (solo lo aceptado)
         \                          /
release/hito-01 ──●────●────●──────●  ← ✋ aceptación en lote = fusión a master
                  ↑    ↑    ↑
              tarea-001  tarea-002  tarea-003   (cada una, PR ✋ a la release)
```

- **Una rama release por hito**, creada desde la rama principal al aprobarse el hito. Solo hay **una release activa** a la vez.
- **Una rama y una PR por tarea o paquete**, que sale de la release y vuelve a ella. La fusión requiere aprobación humana.
- La release es donde se integra y prueba el hito completo.
- **Aceptación en lote = fusionar la release a la rama principal.** Lo que está en la rama principal es exactamente lo aceptado.
- Las correcciones urgentes sobre la rama principal (hotfix) quedan fuera del esqueleto (punto abierto).

### Sin worktrees: una sola carpeta de trabajo
- **Un solo agente que escribe código a la vez**, de forma secuencial (rama → tests → implementa → PR → vuelve a la release).
- **Solo el desarrollador cambia de rama.** El resto de agentes nunca hace `checkout`/`switch` (lo impide un hook).
- Los agentes que no programan **leen el código por referencia**, sin tocar la carpeta de trabajo:
  - por defecto la release o la rama principal; si necesitan el trabajo de una tarea, la **rama que consta en su fichero de estado**;
  - con `git show <rama>:<ruta>`, `git grep <texto> <rama>`, `git diff <base>...<rama>`.
  - Solo ven lo commiteado; lo que el desarrollador tenga a medias no es visible (es deseable: no se diseña sobre trabajo a medias).
- En paralelo solo lo que no toca código: análisis, diseño, maquetas, validación, revisión de PRs.

### Protección
- **Ningún agente fusiona a la rama principal ni a `release/*`, ni despliega.** Dos capas:
  1. **Hooks locales**: bloquean `git push` a ramas protegidas, `git merge` sobre ellas, `gh pr merge` y el cambio de rama fuera del desarrollador. Dan un error inmediato y claro al agente.
  2. **Protección de rama en GitHub** sobre la rama principal y `release/*` (PR obligatoria, sin push directo). Es la barrera real. Nota: en repos privados requiere plan de pago; si no está disponible, solo queda la capa de hooks.
- Presupuesto por tarea, permisos por rol y trazabilidad de quién hizo qué.

---

## 13. Implementación en Claude Code (propuesta)

| Pieza del diseño | En Claude Code |
|---|---|
| Orquestador | Sesión principal arrancada como agente propio, con lista de subagentes permitidos |
| Agentes por rol | Subagentes en `.claude/agents/*.md` con prompt, herramientas, **modelo** y esfuerzo |
| Conocimiento por stack | Skills, precargables en cada subagente |
| Permisos y límites | Herramientas permitidas por agente y hooks (§12, Protección) |
| Tablero | Capa de estado sobre `.factory/estado/`; más adelante GitHub vía MCP |
| Memoria / decisiones | `CLAUDE.md` + `.factory/`; memoria persistente por agente si hace falta |
| Distribución | Empaquetado como plugin (desde este repositorio) |

**Limitaciones a tener en cuenta**:
- Los subagentes no pueden preguntar directamente al usuario. Encaja con la regla de que escalan al orquestador, pero el **agente de descubrimiento** necesita conversar con el humano → debe ser una sesión propia o un modo del orquestador, no un subagente.
- Los subagentes no pueden lanzar otros subagentes → el orquestador tiene que ser la sesión principal.

**Modelos**: elegibles por agente dentro de la familia Claude.

### Orden de construcción propuesto (pendiente de confirmar)
1. Esqueleto: orquestador + analista + arquitecto + desarrollador + validador, `.factory/` con backend de ficheros y ciclo reducido, modelo de ramas y hooks.
2. Tablero en GitHub Projects (segundo backend detrás de la misma capa).
3. Descubrimiento, roadmap por hitos y arquitectura base.
4. Skills por stack (empezando por dos muy distintos).
5. Vista HTML local y maqueta navegable.

---

## 14. Decisiones tomadas

| Decisión | Motivo |
|---|---|
| Ciclo de vida reducido para el esqueleto | Validar el flujo con menos máquina de estados; mismos puntos de decisión humana |
| Primer backend: ficheros `.md` en `.factory/estado/` | El estado debe persistir desde el día uno; valida la capa de backend con dos implementaciones |
| Artefactos y estado en `.factory/`, local y sin versionar; el repo solo para entregables | Evita que los cambios de rama afecten a análisis y diseño sin recurrir a worktrees |
| Sin worktrees; lectura de código por referencia a rama | Los worktrees son difíciles de gestionar para un humano |
| Un solo usuario por proyecto | Simplicidad; exponer el estado a otros queda para el futuro |
| Ramas: release por hito, tareas contra la release, aceptación en lote = fusión a la rama principal | El punto de decisión del hito tiene reflejo exacto en git |
| Rechazos en el lote se corrigen dentro de la release | Evita reverts sobre código ya integrado; el revert queda como excepción |
| Protección en dos capas: hooks + protección de rama en GitHub | Los hooks no cubren todas las vías |
| Tests antes de implementar, escritos por el desarrollador; sin agente tester | Tests definidos por el *qué*; independencia garantizada por el validador y el commit previo de los tests |

---

## 15. Puntos abiertos

- Confirmar el orden de construcción.
- Valor de N (reintentos antes de bloquear) y límites de presupuesto.
- Formato concreto de cada artefacto, de los ficheros de estado y del perfil de proyecto.
- Qué dos stacks se usan para validar la abstracción, y proyecto piloto con el que probar el esqueleto.
- Flujo de hotfix sobre la rama principal.
- Si algún día hay más personas: cómo exponer el estado y compartir los artefactos.
- Si las vistas pasarán en el futuro a permitir acciones (aprobar, mover, reasignar).
