# Estrategia de pruebas

**Estado:** borrador v0.1

## Principios

- Las pruebas deben verificar comportamiento observable y proteger los flujos críticos, no la estructura interna del código.
- Cada cambio debe tener pruebas proporcionales al riesgo y a los criterios de aceptación.
- No se exige un porcentaje global de cobertura. Cada perfil puede definir objetivos útiles para su proyecto, pero la cobertura no sustituye a pruebas de comportamiento.
- Las pruebas deben ser reproducibles, aisladas y ejecutables siguiendo la documentación del proyecto.
- Usar datos sintéticos o anonimizados; nunca incluir credenciales ni datos personales reales en fixtures o logs de pruebas.

## Capas de prueba

- **Estáticas:** formato, lint, análisis de tipos y análisis estático que correspondan al perfil.
- **Unitarias:** reglas de negocio y funciones que se puedan comprobar de forma aislada.
- **Integración:** interacción entre módulos, base de datos, servicios, permisos y contratos.
- **Extremo a extremo:** recorridos principales desde la perspectiva del usuario o cliente; reservarlos para flujos de alto valor y riesgo.

No todos los cambios necesitan todas las capas. La persona responsable debe ejecutar las pruebas afectadas por el cambio y la CI debe ejecutar los controles requeridos antes de integrar.

## Requisitos por perfil

### Aplicaciones iOS y Android

- Cubrir con pruebas unitarias las reglas de negocio y transformaciones críticas.
- Probar de extremo a extremo los recorridos esenciales, como inicio de sesión, acciones principales y persistencia cuando apliquen.
- Incluir estados de error, falta de conexión y permisos del sistema cuando sean relevantes para el flujo.
- Antes de una release, validar los builds en las versiones declaradas como soportadas: iOS 16 y la versión más reciente objetivo; Android, las dos versiones principales más recientes.
- Mantener separada la validación de la API objetivo exigida por Google Play de la matriz de versiones Android soportadas.

### Juegos

- Probar las reglas y sistemas de juego de forma determinista cuando sea posible, separándolos de renderizado, entrada y tiempo real.
- Validar los recorridos esenciales de inicio, partida, pausa o reanudación y guardado/carga si existen.
- Antes de publicar, comprobar que el build arranca y que los controles y el progreso funcionan en cada plataforma declarada.

### Aplicaciones React web

- Usar Vitest y Testing Library para probar comportamiento de componentes y reglas de negocio en el nivel apropiado.
- Usar Playwright para cubrir de extremo a extremo los recorridos principales y sus errores relevantes.
- Comprobar navegación por teclado y nombres accesibles en controles interactivos importantes.
- CI debe ejecutar ESLint, chequeo de tipos, Vitest, Playwright y build.

### APIs REST

- Validar que el contrato OpenAPI coincide con las rutas y respuestas implementadas.
- Probar integración para entradas válidas e inválidas, autenticación, autorización, errores y persistencia cuando aplique.
- Verificar compatibilidad hacia atrás al modificar contratos existentes; los cambios incompatibles deben seguir la política de versionado.
- No probar contra servicios de producción ni usar credenciales o datos reales.

### Módulos PrestaShop

- Probar instalación, configuración, guardado y validación de opciones del módulo.
- Probar hooks, controladores y permisos que sean parte de los flujos del módulo.
- Si hay cambios de esquema, probar instalación y actualización, además del comportamiento esperado al desinstalar.
- Probar al menos la versión mínima soportada (PrestaShop 8.2) y las versiones adicionales declaradas en la matriz del módulo.
- Revisar la interfaz conforme a la [guía visual de módulos PrestaShop](../prestashop/UI_GUIDELINES.md).

## CI y releases

- En cada rama de tarea, ejecutar comprobaciones estáticas y pruebas relacionadas con los archivos o comportamientos afectados.
- Antes de integrar, CI debe pasar y los criterios de aceptación deben estar cubiertos por comprobaciones automatizadas o una revisión manual documentada cuando automatizarlos no sea razonable.
- Antes de una release, ejecutar la matriz completa de compatibilidad declarada y una prueba de humo del build o despliegue candidato.
- En cambios críticos, la prueba de humo debe cubrir como mínimo que la aplicación inicia, el flujo principal funciona y no aparecen errores bloqueantes.
- Las pruebas inestables deben corregirse o registrarse para seguimiento; no se deben ocultar fallos con reintentos automáticos indefinidos.

## Documentación del proyecto

Cada proyecto debe indicar cómo ejecutar sus pruebas, qué servicios o datos de prueba requiere y qué matriz de versiones se comprueba en CI y antes de publicar.
