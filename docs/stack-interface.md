# Interfaz de stack (borrador para definir)

La plataforma no sabe de tecnologías: las aprende de un **paquete de stack** que se elige al iniciar el proyecto. Este documento recoge **qué tiene que declarar un stack** para que la plataforma lo lea y alimente con él a los agentes. Es la lista de lo que hay que definir; el formato final se decide al hacer B07.

## Cómo se conecta (propuesta)

- Cada stack es una carpeta `stacks/<id>/` dentro del plugin (o en `~/.factory/stacks/` para los propios).
- Un fichero **declarativo** `stack.json` que lee el comando `factory` (y el panel): datos y switches, sin prosa.
- Instrucciones **por rol** en Markdown (`agents/<rol>.md`) que cada agente lee además de las suyas, igual que hoy lee `shared/agent-rules.md`.
- Plantillas propias (`templates/`) y, si hace falta, un esqueleto de proyecto (`scaffold/`).
- El proyecto guarda `stack: <id>` y `stack_version` en su perfil al iniciarse (`factory init --stack <id>`). `factory stack show` imprime lo que aplica al proyecto.
- Sin stack (`stack: none`), todo funciona como hoy: el arquitecto propone el stack en la arquitectura base.

## Qué declara un stack

### 1. Identidad
- `id`, nombre, versión del paquete y descripción de una línea (para elegirlo en el arranque).
- **Para qué sirve** y para qué no: tipo de producto, tamaño adecuado, cuándo recomendarlo. Lo usa el orquestador para proponerlo en el descubrimiento.
- **Requisitos de la máquina**: herramientas que tienen que estar instaladas (node, python, sf CLI, Xcode…) y cómo comprobarlas. `factory init` las verifica y avisa.

### 2. Interfaz
- **Tipo de interfaz**: web, app móvil, escritorio, plataforma (Salesforce, Shopify…), línea de comandos o ninguna. Sustituye al actual `interface: web`.
- **Tamaños de pantalla** que hay que diseñar y validar (móvil y escritorio, tableta, solo escritorio…).
- **Accesibilidad** exigida (p. ej. WCAG AA) y cómo se comprueba.

### 3. Diseño
- **Si el diseño aplica** y qué niveles tienen sentido (completo, directrices, ninguno).
- **Medio de maqueta**: HTML (por defecto, válido para casi todo), o el propio de la plataforma si lo hay.
- **Herramientas de diseño recomendadas** (Claude Design, plugin `frontend-design`…) y cuáles no encajan.
- **Sistema de componentes de la plataforma** que hay que respetar (p. ej. SLDS en Salesforce, Material en Android) y si limita lo que se puede diseñar.
- **Cómo pasan los tokens al código**: a CSS, a un tema de la app, a variables de la plataforma… Con su tarea transversal tipo y la comprobación que hará el validador.

### 4. Estructura y comandos
- **Esqueleto** del repositorio y convenciones (carpetas, nombres, idioma del código).
- **Comandos** que hoy rellena el arquitecto en el perfil: install, build, test, test de un fichero, lint, run. Pasan a venir del stack; el arquitecto solo los ajusta.
- **Ramas y CI**: plantilla de CI, comprobaciones obligatorias en las PR y protección de ramas.

### 5. Pruebas
- **Cómo se trazan** tests y criterios (`AC-F001-02` en el nombre del test) en ese framework.
- **Niveles**: unitarias, de integración y de interfaz (navegador sin interfaz, simulador, org de pruebas…), y cuáles son obligatorias.
- **Qué comprueba el validador** además de los tests: accesibilidad, rendimiento, seguridad, cobertura mínima, reglas de la plataforma.

### 6. Vista previa
- **Tipo**: ficheros estáticos (`static`, con la carpeta que se sirve), servidor de desarrollo (`url`, con el comando que lo arranca) o ninguna.
- Para ramas de tarea y release: si se puede previsualizar sin desplegar y cómo.
- El panel muestra la pestaña «Vista previa» solo si el stack la tiene.

### 7. Entorno de pruebas y despliegue (enlaza con la nota 17)
- **Entornos**: pruebas, preproducción, producción; cuáles existen y quién los crea.
- **Cómo se despliega** a cada uno (comando, servicio, GitHub Pages, tienda de apps, org de Salesforce…) y qué credenciales o cuentas hacen falta (siempre del humano, nunca en el repositorio).
- **Qué aprobación humana** exige cada despliegue: hoy la regla es «ningún agente despliega»; el stack dice qué puede automatizarse (p. ej. pruebas) y qué no (producción).
- **Vuelta atrás**: cómo se revierte un despliegue.

### 8. Entregables específicos
- **Maqueta interactiva** (B06): si se entrega HTML, una build de prueba (TestFlight, APK) o un enlace a un entorno.
- **Demo** (nota 16): cómo se graba o se enseña en ese stack.
- **Documentación técnica** que se entrega al cliente con el código (manual de despliegue, de administración…).

### 9. Instrucciones por rol
Lo que cada agente necesita saber del stack, en `agents/<rol>.md`:

| Rol | Qué recibe del stack |
|---|---|
| Orquestador | Cuándo recomendar el stack, preguntas propias del descubrimiento (p. ej. «¿tienes org de Salesforce?»), qué material pedir al cliente |
| Analista | Restricciones que afectan a la especificación (límites de la plataforma, qué es configurable y qué no) |
| Prototipador / diseño | Medio de maqueta, componentes de la plataforma, tamaños, cómo pasar los tokens |
| Arquitecto | Arquitectura de referencia, transversales tipo del primer hito (esqueleto, CI, tokens, despliegue a pruebas), patrones y antipatrones |
| Desarrollador | Convenciones de código, cómo escribir los tests primero en ese framework, librerías permitidas, plugin de diseño a usar |
| Validador | Cómo ejecutar y comprobar cada nivel de prueba, la lista de revisión específica de la plataforma |

## Por decidir contigo

1. ¿Formato del declarativo (`stack.json`) o todo en Markdown con una cabecera?
2. ¿Qué stacks primero? Propuesta: `web-static` (como Boadilla Motor) y uno sin interfaz para comprobar que el núcleo no depende de la web.
3. ¿Se elige el stack en el arranque (con la pregunta del nombre e idioma), en el descubrimiento o lo propone el arquitecto? ¿Se puede cambiar después?
4. ¿Los stacks propios del estudio viven en `~/.factory/stacks/`, en un repositorio aparte o como plugins?
5. ¿Hasta dónde llega el despliegue automático y con qué aprobación?
