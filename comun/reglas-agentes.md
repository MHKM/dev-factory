# Reglas comunes de los agentes de factory

Estas reglas se aplican a todos los agentes. Las de tu rol están en tu propio prompt.

## Dónde está cada cosa

```
<proyecto>/
  …                     ← entregables (código, tests, configuración): ramas y PRs
  .factory/             ← local, en .gitignore, nunca se commitea
    proyecto.md         ← perfil: stack, comandos, convenciones, rama principal, remoto
    estado/             ← un .md por hito (H01), funcionalidad (F001) y tarea (T001)
    artefactos/         ← vision.md, roadmap.md, arquitectura.md y una carpeta por elemento
      H01/  diseno.md, lote.md
      F001/ spec.md, reglas-negocio.md, maqueta/index.html, diseno.md, validacion.md
      T001/ revision.md
    decisiones/         ← D001-….md: registro de decisiones
    tmp/                ← exportaciones de ramas (`factory exportar`)
```

`factory rutas <ID>` te da las rutas exactas de los artefactos de un elemento.

## Estado: solo a través del comando `factory`

Nunca edites a mano el frontmatter de `.factory/estado/` ni `.factory/proyecto.md`. Usa:

| Para | Comando |
|---|---|
| Ver un elemento y sus artefactos | `factory ver <ID>` |
| Empezar a trabajar en algo | `factory situacion <ID> en_curso` y `factory set <ID> agente=<tu rol>` (solo tareas) |
| Cambiar de fase (vuelve a `en_cola`) | `factory fase <ID> <fase>` |
| Cambiar campos | `factory set <ID> campo=valor …` |
| Crear elementos | `factory nuevo hito|func|tarea --titulo … [--texto -]` (imprime el ID) |
| Preguntar al humano | `factory preguntar <ID> --agente <rol> --texto - <<'EOF' … EOF` |
| Contar un intento fallido | `factory intento <ID> --motivo "…"` |
| Leer otra rama sin cambiar de rama | `factory exportar <rama>` (devuelve una carpeta) |

El proyecto en sí se referencia con el ID `proyecto`.

**Al terminar, deja siempre el elemento en un estado coherente**: o lo avanzas de fase, o lo dejas en `esperando_humano` con preguntas, o en `en_cola` con un motivo. Nunca lo dejes en `en_curso`.

## Preguntar en lugar de inventar

- Ante una decisión relevante que no esté ya resuelta en `.factory/decisiones/`, en la arquitectura base o en la especificación, **no la tomes tú**: pregunta.
- No hablas con el humano. Escribes las preguntas con `factory preguntar` y terminas. El orquestador se las presenta.
- Formato de cada pregunta:

  ```markdown
  **P1. <pregunta concreta>**
  - **A) <opción>** — <consecuencia>. *(Recomendada: <por qué>)*
  - **B) <opción>** — <consecuencia>.
  ```

- Agrupa todas las preguntas en una sola llamada. Haz las mínimas y solo las que cambian el resultado.
- Si puedes avanzar en parte sin la respuesta, avanza, y deja dicho qué queda pendiente.

## Antes de actuar

1. Lee `.factory/proyecto.md` (stack, comandos, convenciones).
2. Lee el elemento con `factory ver <ID>` y los artefactos de los que depende.
3. Revisa `.factory/decisiones/` (los títulos y lo que te afecte). Una decisión registrada manda sobre tu criterio.

## Git

- **Solo el desarrollador cambia de rama.** El resto lee otras ramas con `git show <rama>:<ruta>`, `git grep <texto> <rama>`, `git diff <base>...<rama>` o `factory exportar <rama>`. La rama de cada tarea consta en su estado (`rama`); la release del hito, en el estado del hito.
- Ningún agente fusiona en la rama principal ni en `release/*`, ni hace `gh pr merge`, ni despliega. Un hook lo bloquea.
- Los artefactos de `.factory/` nunca se commitean.

## Estilo

- Escribe en español, claro y breve. Los artefactos son para que un humano decida rápido: nada de relleno.
- Usa las plantillas de la carpeta `plantillas/` del plugin (la ruta exacta está en tu prompt).

## Respuesta final al orquestador

Termina siempre con este bloque, sin más:

```
RESULTADO: <hecho | preguntas | bloqueado | parcial>
ELEMENTOS: <IDs tocados y su fase/situación final>
RESUMEN: <2-4 líneas: qué has hecho y qué necesita atención>
```
