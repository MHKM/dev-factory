# Arquitectura base

> Solo decisiones estructurales. Cada hito diseña dentro de este marco; cambiarlo exige una decisión explícita (D###).

## Stack
| Pieza | Elección | Decisión |
|---|---|---|
| <frontend / backend / datos / hosting / tests> | <tecnología y versión> | D### |

## Estructura
<Componentes principales y cómo se relacionan. Un diagrama ASCII si ayuda.>

```
<carpetas de primer nivel del repositorio y para qué sirve cada una>
```

## Modelo de datos principal
<Entidades clave y relaciones. Solo lo estructural.>

## Integraciones externas
<Servicios de terceros, cómo se usan, credenciales necesarias (nunca en el repo).>

## Estrategia de pruebas
<Tipos de test, herramienta, cómo se trazan con los criterios de aceptación (p. ej. el nombre del test incluye AC-F001-01).>

## Entornos y despliegue
<Local, pruebas, producción. Quién despliega (nunca un agente).>

## Riesgos y supuestos
- <supuesto que, si falla, obliga a revisar esta arquitectura>
