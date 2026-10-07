---
name: createapp
description: "Crear una aplicación con componentes API, web o móvil en la raíz de desarrollo configurada."
argument-hint: "Nombre y componentes deseados"
agent: agent
---

Crea un proyecto de tipo `app` usando el generador compartido. La aplicación puede combinar los componentes `api`, `web`, `mobile`, `ios` y `android`.

1. Si faltan datos, pregunta el nombre del proyecto y los componentes. El nombre debe usar minúsculas y kebab-case.
2. No preguntes la ruta: el generador calcula el destino bajo la raíz de desarrollo configurada. No preguntes la visibilidad: los repositorios siempre son privados. Usa el propietario de GitHub autenticado, salvo que el usuario indique una organización.
3. Localiza `scripts/create-project.sh` en el repositorio de estándares o `.dev-standards/scripts/create-project.sh` si está instalado en el proyecto. No recrees manualmente lo que hace el generador.
4. Ejecuta primero `--dry-run`, informa el nombre, componentes, destino y propietario que se usarán, y pide confirmación explícita antes de crear archivos o un remoto.
5. Tras confirmar, ejecuta el generador con `--type app`, `--name` y `--components`. Usa `--owner` solo si se indicó una organización.
6. Si GitHub CLI no está instalado o autenticado, no simules un remoto; explica el problema y pregunta si se desea crear solo localmente con `--no-remote`.

El generador crea el esqueleto de estándares y metadatos; no elige ni instala un framework o tecnología de aplicación sin una decisión explícita del usuario.