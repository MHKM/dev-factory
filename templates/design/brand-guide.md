# Guía de marca y diseño · <nombre del proyecto>

> Kit de diseño del proyecto: esta guía, `tokens.json` (fuente única de los valores), `tokens.css` (generado con `factory tokens`) y la galería `index.html` (se ve desde el panel).
> Nivel: **completo** / **directrices** (en «directrices» bastan las secciones marcadas con ★).

## 1. Concepto ★
**Personalidad:** <3-4 adjetivos: cercana, fiable, profesional…>
**Qué debe transmitir:** <en una frase, a quién y qué sensación>
**Referencias:** <webs o marcas que gustan, y qué se toma de cada una>

## 2. Logotipo
- **Versiones:** principal, horizontal, símbolo, monocromo (positivo/negativo). <rutas a los ficheros o "pendiente de aportar">
- **Área de respeto:** <p. ej. la altura de la letra X alrededor del logo>
- **Tamaño mínimo:** <px en pantalla / mm en impresión>
- **Usos incorrectos:** no deformar, no cambiar colores, no poner sobre fondos con poco contraste, no añadir sombras.

## 3. Color ★
| Rol | Token | HEX | Pantone (aprox.) | CMYK | Uso |
|---|---|---|---|---|---|
| Primario | `color.primary` | #… | … | … | Acción principal, enlaces |
| Acento | `color.accent` | #… | … | … | CTA destacada, con moderación |
| Texto | `color.text` | #… | — | — | Texto principal |
| … | | | | | |

- **Proporción orientativa:** 60 % neutros · 30 % marca · 10 % acento.
- **Accesibilidad:** todo texto cumple contraste WCAG AA (4,5:1; 3:1 en texto grande). La galería lo calcula.
- **Pantone y CMYK** son equivalencias aproximadas para impresión: confirmar con una guía física antes de imprimir.
- **Modo oscuro:** <sí/no; si sí, los valores están en `$extensions.mode.dark` de cada token>

## 4. Tipografía ★
| Uso | Familia | Pesos | Licencia |
|---|---|---|---|
| Titulares | `font.family.heading` | … | … |
| Texto | `font.family.body` | … | … |

- **Escala:** `font.size.xs` … `font.size.4xl` (ratio <1,25>). H1 = `4xl` en escritorio / `3xl` en móvil; texto = `md`.
- **Interlineado:** `tight` en titulares, `normal` en texto. Longitud de línea: 60-75 caracteres.

## 5. Espaciado, retícula y breakpoints ★
- **Espaciado:** escala `space.*` (base 4px). No usar valores fuera de la escala.
- **Retícula:** <12 columnas en escritorio, 4 en móvil>, ancho máximo `layout.max-width`, margen lateral `layout.gutter`.
- **Breakpoints:** `breakpoint.sm/md/lg/xl`, diseño mobile first.

## 6. Forma y profundidad
- **Radios:** `radius.sm` (inputs), `radius.md` (botones, tarjetas), `radius.lg` (bloques destacados), `radius.pill` (etiquetas).
- **Sombras:** `shadow.sm` (tarjetas en reposo), `shadow.md` (elementos elevados, menús).
- **Movimiento:** transiciones `motion.fast`/`motion.normal`; nada de animaciones que distraigan.

## 7. Iconografía
<Estilo (línea/relleno), grosor, librería recomendada y su licencia, tamaños (16/20/24px).>

## 8. Fotografía e ilustración
<Estilo de las imágenes (reales del negocio, luz natural…), qué evitar (bancos de imágenes genéricos), tratamiento, proporciones habituales.>

## 9. Componentes
Se ven en la galería. Para cada uno: variantes, estados (reposo, hover, foco, deshabilitado, error) y cuándo usarlo.
- **Botones:** primario (una sola acción principal por vista), secundario, texto.
- **Formularios:** campo, etiqueta siempre visible, ayuda, error en `color.danger` con mensaje.
- **Tarjetas, cabecera y navegación, pie, avisos (éxito, aviso, error).**

## 10. Tono de voz ★
<Tú/usted, frases cortas, vocabulario del cliente; ejemplos de titular, botón y mensaje de error.>

## 11. Accesibilidad ★
Contraste AA, foco visible en todo lo interactivo, objetivos táctiles ≥ 44px, textos alternativos, no transmitir información solo con color.

## 12. Entregables
| Fichero | Para qué |
|---|---|
| `tokens.json` | Fuente única de los valores (W3C Design Tokens) |
| `tokens.css` | Variables CSS listas para usar (generado) |
| `index.html` | Galería visual: colores, tipografía, espaciado, componentes |
| `brand-guide.md` | Esta guía |
| `assets/` | Logos y recursos aportados (si los hay) |
