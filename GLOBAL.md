# Principios globales

**Estado:** borrador v0.1

Este documento define cómo interpretar y combinar los estándares aplicables a todos los proyectos. Los requisitos globales se complementan con perfiles tecnológicos y decisiones específicas de cada proyecto.

## Niveles de obligatoriedad

- **MUST:** requisito obligatorio. Si afecta a una publicación, debe cumplirse antes de publicar.
- **SHOULD:** comportamiento recomendado. Si un proyecto se desvía, debe documentar la razón y las medidas alternativas.
- **MAY:** opción permitida, que el proyecto puede adoptar cuando resulte útil.

Los documentos deben usar estas palabras de forma consistente. Una recomendación no debe presentarse como bloqueo automático de CI si no existe una comprobación que la haga cumplir.

## Jerarquía de requisitos

Al resolver una contradicción, aplicar este orden:

1. Las leyes, requisitos de plataforma o tienda y obligaciones contractuales aplicables.
2. Los requisitos globales obligatorios de este repositorio, incluidos los bloqueos de publicación no negociables.
3. El perfil del tipo de proyecto o tecnología, que concreta cómo aplicar el estándar común y puede imponer controles más estrictos.
4. La configuración y documentación local del proyecto, que pueden añadir requisitos y seleccionar perfiles aplicables.
5. Las plantillas y ejemplos, que orientan, pero no reemplazan los requisitos normativos.

Los niveles más específicos pueden concretar o endurecer un requisito de nivel superior, pero no reducirlo. Si dos documentos del mismo nivel entran en conflicto, se debe registrar el conflicto y resolverlo antes de publicar; no se elige silenciosamente la regla menos estricta.

## Idioma y nombres

- La documentación, los comentarios explicativos y los textos visibles para las personas usuarias se redactan en español.
- Los identificadores internos se escriben en inglés: nombres de variables, funciones, clases, módulos, pruebas, claves de configuración y campos internos de datos.
- Los nombres técnicos de herramientas, comandos, protocolos y APIs conservan la grafía requerida por su tecnología y no se traducen.
- Los nombres propios de productos y proyectos se conservan tal como los defina su responsable; esta regla no obliga a traducirlos.
- Si un producto necesita ofrecer otros idiomas, el español sigue siendo el idioma base y los textos se gestionan mediante el sistema de localización del proyecto.

## Excepciones

Una excepción solo puede aplicarse a un requisito que admita desviación. Debe registrarse junto al contexto del proyecto o en su registro de decisiones e incluir:

- El requisito y los proyectos o componentes afectados.
- La justificación y el riesgo aceptado.
- Las medidas compensatorias, si aplican.
- Quién la aprueba y la fecha de aprobación.
- Una fecha de vencimiento o revisión.

En proyectos personales, el mantenedor puede aprobar su propia excepción, pero debe dejar constancia de la decisión. Las excepciones temporales vencidas deben revisarse antes de la siguiente publicación. Si una excepción pasa a ser habitual, se debe proponer cambiar el estándar o el perfil en vez de perpetuar excepciones locales.

No se permiten excepciones al requisito de cero vulnerabilidades críticas detectadas para publicar. Tampoco se pueden exceptuar obligaciones legales, contractuales o de las tiendas de aplicaciones.

## Uso por proyectos y agentes

- Cada proyecto debe declarar su tipo, componentes y versión de estándares instalados en `.dev-standards/project.yml`.
- Antes de cambiar código, una persona o agente debe identificar los requisitos globales y los perfiles aplicables al proyecto.
- Los agentes no deben debilitar requisitos ni registrar excepciones por su cuenta; deben explicar el conflicto y proponer la decisión al mantenedor.
- Las actualizaciones de estándares se revisan explícitamente en el proyecto consumidor, incluyendo el diff y cualquier impacto en sus personalizaciones.

## Edición de proyectos y actualización de estándares

- Un comando de edición de proyecto debe usar por defecto los estándares locales declarados en `.dev-standards/project.yml`.
- Si detecta que existe una versión más reciente de los estándares, debe informar al mantenedor y ofrecer continuar con la versión instalada, revisar una actualización separada o cancelar.
- Los comandos de edición no deben actualizar estándares automáticamente ni mezclar una actualización de estándares con cambios funcionales del proyecto.
- Un comando de actualización debe mostrar el diff y los posibles conflictos con personalizaciones locales antes de aplicar cambios. La modificación requiere confirmación explícita.
- Mantener separables los cambios de actualización de estándares y los cambios funcionales para poder revisarlos y revertirlos de manera independiente.
