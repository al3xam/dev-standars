# Estándares de calidad para proyectos

**Estado:** borrador v0.1

Este repositorio define una base común de calidad para proyectos personales: aplicaciones, juegos, sitios web, APIs y módulos de PrestaShop. Los requisitos comunes aplican a todos; cada perfil tecnológico añade sus propias reglas y matriz de compatibilidad.

La jerarquía de requisitos, los niveles de obligatoriedad y el proceso de excepciones se definen en [GLOBAL.md](GLOBAL.md).

## Principios

- Los requisitos deben ser verificables siempre que sea posible.
- La CI debe ejecutar las comprobaciones aplicables al proyecto antes de publicar.
- No se impone una única tecnología ni un porcentaje global de cobertura de pruebas.
- Cada proyecto declara sus tecnologías, versiones soportadas e instrucciones para instalar, probar y publicar.

## Organización y creación de proyectos

Los proyectos se organizan por tipo bajo una raíz configurable, sin fijar una ruta personal en el repositorio:

```text
<DEVELOPMENT_ROOT>/
├── apps/
├── games/
├── websites/
├── prestashop/
└── tooling/
	└── project-standards/
```

La ubicación por tipo es `apps/<nombre>`, `games/<nombre>`, `websites/<nombre>` o `prestashop/<nombre>`. Una ruta explícita indicada al crear el proyecto tiene prioridad sobre la ubicación automática.

Los nombres de proyectos y carpetas usan minúsculas y kebab-case. El tipo define la ubicación; los componentes describen las partes del proyecto y no fuerzan una tecnología. Tipos iniciales: `app`, `game`, `website` y `prestashop`.

| Proyecto | Tipo | Componentes | Ubicación |
| --- | --- | --- | --- |
| `repost-app` | `app` | `api`, `mobile`, `ios`, `android` | `apps/repost-app/` |
| `juego-movil` | `game` | `ios`, `android` | `games/juego-movil/` |
| `inventario-api` | `app` | `api` | `apps/inventario-api/` |
| `tienda-web` | `website` | `web` | `websites/tienda-web/` |
| `modulo-envios` | `prestashop` | — | `prestashop/modulo-envios/` |

Un backend permanece como componente de una `app` cuando comparte producto y ciclo de desarrollo con las aplicaciones cliente. Se crea como proyecto separado cuando necesita un ciclo de despliegue o mantenimiento independiente. El tipo `game` identifica un juego, pero no prescribe el motor ni el lenguaje; `ios` y `android` indican sus plataformas objetivo.

El comando de creación de proyectos debe:

- Crear el directorio local, instalar una copia local de los estándares y generar el manifiesto del proyecto.
- Generar `.gitignore` con reglas comunes y añadir perfiles web/iOS/Android según tipo y componentes.
- Instalar los prompts de VS Code en `.github/prompts/` y conservar una copia del generador en `.dev-standards/scripts/`.
- Inicializar Git, crear un commit inicial y dejar las ramas `main` y `develop` listas para trabajar.
- Crear el repositorio remoto de GitHub y configurarlo como `origin`. Todos los repositorios creados deben ser privados; no se ofrece una opción pública.
- Comprobar primero que no existan ya el directorio ni el remoto, y detenerse sin sobrescribirlos.
- Usar GitHub CLI autenticado para crear el remoto. Si falla una operación remota, conservar el proyecto local y explicar cómo reintentar.
- Proteger `main` contra force-push y borrado si GitHub y los permisos lo permiten; si no, informar que la protección no se aplicó.
- Permitir seleccionar propietario y ruta explícita, u omitir la creación remota.

El creador está disponible mediante `scripts/create-project.sh`:

```sh
./scripts/create-project.sh --type app --name repost-app --components api,mobile,ios,android --dry-run
./scripts/create-project.sh --type app --name repost-app --components api,mobile,ios,android
./scripts/create-project.sh --type app --name repost-app --components api,mobile,ios,android --no-remote
```

`--dry-run` valida y muestra las acciones sin crear archivos. `--path` establece una ubicación exacta; en su ausencia, `--root` o `DEV_STANDARDS_DEVELOPMENT_ROOT` definen la raíz organizada por tipo. `--owner` selecciona un usuario u organización de GitHub; por omisión se usa la cuenta autenticada. Los remotos se crean siempre como privados. La creación remota requiere GitHub CLI autenticado (`gh auth login`). `--no-remote` crea solo el proyecto local.

Para crear el commit inicial, Git debe tener `user.name` y `user.email` configurados explícitamente en la configuración global.

## Prompts de VS Code

Los prompts fuente están en `.github/prompts/` y se copian a cada proyecto nuevo. Están disponibles como `/createapp`, `/creategame`, `/createweb`, `/createmodule`, `/editproject` y `/updatestandards`. Para que VS Code los detecte desde este repositorio, abrir `project-standards` como carpeta de workspace.

La raíz de desarrollo debe poder configurarse mediante una opción del comando o una variable de entorno. La configuración con rutas personales no debe versionarse.

Cada proyecto debe guardar su manifiesto en `.dev-standards/project.yml`, generado a partir de [`templates/project.yml`](templates/project.yml):

```yaml
schema_version: 1

project:
	name: repost-app
	type: app
	components:
		- api
		- mobile
		- ios
		- android

standards:
	version: "0.1.0"
```

`schema_version` identifica el formato del manifiesto; `standards.version` registra la versión SemVer de los estándares instalados. `project.name` usa kebab-case, `project.type` determina la carpeta y `project.components` enumera solo los componentes aplicables. El comando de creación debe generar el manifiesto con los valores elegidos y la versión de estándares instalada.

## Requisitos comunes

- El proyecto debe poder instalarse y compilarse desde un clon limpio siguiendo su documentación.
- Los chequeos automáticos de formato y análisis estático deben pasar en CI.
- Deben existir pruebas para los flujos y reglas de negocio críticos. Cada perfil podrá fijar su umbral de cobertura.
- Los secretos y credenciales no deben almacenarse en el repositorio.
- La documentación debe reflejar los cambios que afecten a instalación, configuración, uso o contratos públicos.
- Cada tarea debe registrar su objetivo y criterios de aceptación en el issue o sistema de seguimiento correspondiente.
- Las publicaciones deben usar SemVer: `PATCH` para correcciones compatibles, `MINOR` para funcionalidad compatible y `MAJOR` para cambios incompatibles.
- Cada publicación debe tener una versión identificable y notas de cambios.
- Antes de publicar, el mantenedor debe completar una lista de autocontrol. No se requiere aprobación de otra persona para proyectos personales de un solo desarrollador.
- Los archivos de bloqueo de dependencias deben versionarse cuando el gestor los genere. Las alertas y actualizaciones de dependencias deben revisarse con regularidad y probarse antes de integrarlas.

Las capas y criterios de prueba por perfil, CI y release se detallan en [testing/TESTING.md](testing/TESTING.md).

## Flujo de trabajo

La definición de tareas listas y terminadas, las ramas por tarea, la coordinación de agentes y el proceso de release están en [git/WORKFLOW.md](git/WORKFLOW.md).

## Seguridad

- Una vulnerabilidad crítica detectada en las comprobaciones de publicación bloquea la publicación. No se aceptan excepciones.
- Una vulnerabilidad alta bloquea la publicación salvo que se documente como falso positivo o no explotable. La excepción debe incluir justificación y fecha de revisión.
- Las vulnerabilidades medias y bajas deben registrarse para su seguimiento, pero no bloquean la publicación.

La gestión de secretos, datos personales, dependencias e incidentes se detalla en [security/SECURITY.md](security/SECURITY.md).

## Perfiles y compatibilidad acordada

### Módulos PrestaShop

- La versión mínima de PrestaShop soportada es 8.2.
- Cada módulo debe declarar las versiones de PrestaShop y PHP que soporta.
- La matriz de pruebas debe cubrir las combinaciones de PHP compatibles con las versiones de PrestaShop declaradas, en la medida que permitan las herramientas del proyecto.
- Las pantallas de configuración deben seguir la [guía visual para módulos PrestaShop](prestashop/UI_GUIDELINES.md).
- Al crear cada módulo, definir su distribución (uso propio, distribución directa o PrestaShop Addons) y decidir si necesita un canal de actualización. Si se publica en Addons, comprobar primero sus reglas; un updater de GitHub es opcional y, si se elige, debe ofrecer la actualización para confirmación manual en vez de instalarla automáticamente.

### Aplicaciones iOS

- La versión mínima de iOS soportada es iOS 16.
- Las pruebas deben cubrir iOS 16 y la versión más reciente que declare soportada el proyecto.

### Aplicaciones Android

- Deben ser compatibles con las dos versiones principales más recientes de Android.
- La matriz de soporte y pruebas debe actualizarse cuando se publique una nueva versión principal de Android.
- El nivel de API objetivo exigido por Google Play se documentará por separado, ya que puede cambiar independientemente de la matriz de compatibilidad.

### Aplicaciones React web

- Las aplicaciones nuevas deben usar TypeScript.
- Usar la última versión estable de React disponible al iniciar el proyecto y fijarla mediante el lockfile.
- Usar una versión LTS activa de Node.js; declarar el rango soportado en `package.json` y fijar la versión de desarrollo en `.nvmrc`. Actualizar antes de que deje de recibir soporte.
- El lockfile debe estar versionado y CI debe instalar dependencias de forma reproducible.
- Usar ESLint para lint, Vitest con Testing Library para pruebas unitarias y de componentes, y Playwright para los flujos principales de extremo a extremo.
- No se impone un framework web global; se elige según las necesidades del proyecto.
- CI debe ejecutar lint, chequeo de tipos, pruebas y build.
- Las pruebas deben cubrir componentes y flujos principales.
- La interfaz debe cumplir criterios básicos de accesibilidad, incluyendo navegación por teclado y etiquetas accesibles.

### APIs REST

- El contrato OpenAPI debe mantenerse versionado junto al código.
- Las entradas deben validarse y las respuestas de error deben seguir un formato consistente.
- La autenticación y autorización deben implementarse cuando corresponda al recurso.
- Los cambios deben preservar la compatibilidad hacia atrás; los cambios incompatibles deben versionarse.
- Las pruebas de contrato e integración deben cubrir flujos críticos, permisos y entradas inválidas.
- Los logs no deben exponer secretos ni datos personales.

### Operación y recuperación

- Los proyectos que almacenen datos de producción deben documentar copias de seguridad y restauración; las restauraciones deben probarse periódicamente.
- Los servicios desplegables deben documentar cómo volver a la versión anterior. Los cambios de esquema de datos deben incluir un plan de recuperación compatible.
- Las aplicaciones móviles deben definir cómo detener o limitar una distribución gradual si se detecta un problema en producción.

## Puerta de publicación

Antes de publicar, debe cumplirse lo siguiente:

- La CI pasa para la configuración declarada por el proyecto.
- Las pruebas de los flujos críticos pasan.
- No hay vulnerabilidades críticas detectadas.
- No hay vulnerabilidades altas sin una excepción documentada.
- La versión y las notas de cambios están actualizadas.
- La documentación afectada está actualizada.

## Pendiente de decisión

- Cómo se automatizará la distribución de actualizaciones de estándares a los repositorios de proyectos.
- Validar creación remota y protección de `main` en un repositorio de prueba de GitHub, sin reutilizar un nombre existente.
