# Guía visual para módulos PrestaShop

**Estado:** borrador v0.1

## Objetivo

Los módulos deben sentirse coherentes dentro del Back Office de PrestaShop. La consistencia se aplica a la estructura, los componentes y los estados de interacción; cada módulo conserva los campos y flujos propios de su función.

## Integración con el Back Office

- Usar el contenedor, navegación, tipografía, componentes y estilos nativos del Back Office compatibles con la versión mínima soportada (PrestaShop 8.2).
- No recrear la navegación global ni sustituir elementos del Back Office.
- Evitar CSS global o selectores que afecten a otras páginas del Back Office. Los estilos propios deben limitarse al contenedor del módulo.
- No introducir una biblioteca visual adicional si los componentes nativos cubren la necesidad.

## Estructura de la página de configuración

Todos los módulos deben compartir el mismo patrón de página:

1. **Cabecera:** título del módulo en la misma ubicación, seguido de una descripción breve de su propósito.
2. **Estado y avisos:** mostrar errores, advertencias o estado de conexión después de la cabecera y antes del contenido al que afectan.
3. **Contenido:** agrupar opciones relacionadas en secciones con títulos descriptivos. Usar pestañas solo cuando existan áreas funcionales diferenciadas y suficientemente amplias.
4. **Acciones:** colocar la acción principal de guardado al final del formulario, en la misma posición y con el mismo estilo en todos los módulos. Las acciones destructivas o secundarias deben estar separadas visualmente y no competir con Guardar.

El patrón común fija la jerarquía y la posición de los elementos, no los campos: cada módulo conserva las secciones y opciones necesarias para su función. Deben preferirse las clases y componentes nativos del Back Office para mantener el patrón compatible.

## Barra superior de navegación y acciones

Todos los módulos deben mostrar, debajo de la cabecera y antes del contenido, una barra horizontal común:

- **Izquierda:** navegación por las áreas funcionales del módulo, como Dashboard, Categorías o Productos. Mantener un orden estable entre páginas del mismo módulo y marcar claramente la sección activa.
- **Derecha:** acciones auxiliares del módulo que correspondan, como Logs, Importar o Sincronizar. Incluir siempre `Configuración` en este grupo.
- **Cron:** colocar la acción o información de Cron junto a las opciones de configuración del grupo derecho solo si el módulo necesita una tarea programada.
- Mostrar únicamente acciones disponibles y útiles para el módulo; no añadir botones de relleno para imitar otros módulos.
- Mantener alineación, tamaño, espaciado, estados activo/deshabilitado e iconografía coherentes en todos los módulos, usando componentes compatibles con PrestaShop 8.2.
- En ventanas estrechas, permitir que los grupos se adapten o envuelvan sin solaparse ni ocultar acciones.
- No duplicar acciones globales del Back Office, como Atrás, Traducir o Configurar los hooks, si PrestaShop ya las muestra en la cabecera.

## Dashboard

Si un módulo tiene estado operativo, sincronizaciones o actividad que ayude a administrarlo, debe ofrecer un Dashboard como primera vista funcional. No se añade un Dashboard vacío a módulos que solo necesiten un formulario de configuración.

La vista debe priorizar la información necesaria para entender el estado actual sin tener que abrir Logs:

1. **Indicadores de resumen:** una fila de tarjetas con métricas clave, por ejemplo estado de conexión, elementos gestionados, categorías activas y fecha de la última actualización correcta. Cada tarjeta incluye una etiqueta clara y un valor legible.
2. **Proceso principal:** cuando exista una sincronización o tarea en curso, mostrar su nombre, estado, progreso, elementos procesados y pendientes. Si no se ha iniciado, mostrar ese estado explícitamente.
3. **Actividad reciente:** mostrar las últimas ejecuciones o actualizaciones relevantes en paneles separados, con fecha, estado y resultado breve. Si todavía no hay actividad, mostrar un estado vacío explicativo.

En escritorio, seguir las proporciones de la referencia visual:

- Distribuir hasta cuatro indicadores relevantes en una fila de tarjetas de igual importancia. Si el módulo tiene menos indicadores útiles, repartirlos en el espacio disponible sin añadir métricas de relleno.
- Mostrar el proceso principal en un panel que ocupe todo el ancho disponible, debajo de los indicadores.
- Mostrar la actividad reciente en dos paneles de igual ancho, debajo del proceso principal. Si solo hay un tipo de actividad relevante, usar un panel ancho en vez de duplicar contenido.
- Mantener visibles los estados y datos operativos principales; el detalle histórico puede quedar en la sección `Logs`.

En pantallas estrechas, apilar los bloques y tarjetas sin perder contexto ni ocultar estados. Usar bordes, espaciado y acentos discretos compatibles con el Back Office, sin depender de colores que comuniquen estado por sí solos.

Los indicadores y paneles deben corresponder a datos reales y útiles del módulo; no se rellenan con métricas decorativas. Las fechas deben identificar claramente cuándo se produjo la última actualización, y los estados no deben comunicarse solo mediante color.

## Formularios y estados

- Cada campo debe tener etiqueta visible y, si requiere aclaración, ayuda breve junto al campo.
- Indicar unidades, formatos esperados y obligatoriedad cuando no sean evidentes.
- Mostrar errores de validación junto al campo correspondiente y resumirlos si hay varios.
- Confirmar el guardado correcto y conservar los valores introducidos cuando ocurra un error.
- Definir estados de carga, vacío, error, éxito y falta de permisos cuando sean aplicables.
- Pedir confirmación antes de acciones destructivas o difíciles de revertir.

## Conexiones externas y credenciales

Cuando el módulo requiera usuario y contraseña u otras credenciales para conectarse a un servicio externo, la sección `Configuración` debe mostrar estados distintos antes y después de validar la conexión:

- **Sin conexión:** mostrar el formulario de credenciales y una acción clara para comprobar la conexión. No mostrar el estado `Conectado` hasta que una comprobación real contra el servicio haya tenido éxito.
- **Conectado:** sustituir el formulario por una tarjeta compacta con el título `Acceso a [servicio]`, un indicador y texto `Conectado`, y las acciones disponibles alineadas a la derecha, siguiendo el patrón de la referencia visual.
- La tarjeta puede ofrecer `Comprobar descarga` u otra verificación funcional equivalente y `Cerrar sesión` para desconectar la cuenta.
- No volver a mostrar la contraseña, token ni secreto después de guardarlos. Si hay que cambiar credenciales, ofrecer una acción explícita para reemplazarlas.
- Al fallar la conexión o caducar la sesión, mostrar el estado y un mensaje accionable; no indicar que la cuenta sigue conectada.
- Mientras se comprueba una conexión o descarga, mostrar progreso y resultado. La verificación funcional debe indicar cuándo fue la última comprobación correcta.
- No registrar credenciales ni respuestas que contengan secretos en errores o logs.

## Accesibilidad, idioma y adaptación

- La interfaz debe poder utilizarse con teclado y conservar un foco visible.
- Asociar etiquetas y mensajes de error con sus campos; no comunicar estados únicamente mediante color.
- Mantener contraste y tamaños legibles usando los estilos nativos.
- Los textos visibles deben ser traducibles y usar el mecanismo de traducción del módulo.
- La página debe seguir siendo usable en ventanas estrechas, sin desbordamientos ni controles inaccesibles.

## Criterios de revisión

Antes de publicar un módulo, comprobar que:

- La página parece parte del Back Office y no altera otras páginas.
- Las secciones y acciones son fáciles de localizar y mantienen una jerarquía consistente.
- La navegación funcional queda a la izquierda; las herramientas, Configuración y Cron, importar o descargar algo cuando aplique quedan a la derecha.
- Si hay Dashboard, muestra indicadores clave, progreso operativo cuando aplique y actividad reciente con estados vacíos explícitos.
- Las conexiones externas muestran formulario hasta validar credenciales y luego una tarjeta de acceso con estado, comprobación funcional y cierre de sesión, sin volver a exponer secretos.
- La cabecera, los avisos y la posición de Guardar coinciden con el patrón usado por los demás módulos.
- Se pueden completar y guardar los formularios, incluidos los casos de error.
- Se puede recorrer y operar la interfaz con teclado.
- La interfaz se ha probado en PrestaShop 9 como versión piloto y también en la versión mínima soportada (8.2), además de las versiones declaradas en la matriz del módulo.
- Los componentes y estilos utilizados están disponibles en todas las versiones soportadas; una prueba visual en PrestaShop 9 no demuestra compatibilidad con 8.2.
