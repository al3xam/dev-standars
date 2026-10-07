---
name: createweb
description: "Crear un proyecto de sitio web con los estándares comunes."
argument-hint: "Nombre del sitio web"
agent: agent
---

Crea un proyecto de tipo `website` bajo `websites/` usando el generador compartido.

1. Si falta, pregunta el nombre del proyecto. Debe usar minúsculas y kebab-case.
2. No preguntes la ruta: el generador calcula el destino bajo la raíz de desarrollo configurada. No preguntes la visibilidad: los repositorios siempre son privados. Usa el propietario de GitHub autenticado, salvo que el usuario indique una organización.
3. Localiza `scripts/create-project.sh` en el repositorio de estándares o `.dev-standards/scripts/create-project.sh` si está instalado. No presupongas Vite, Next.js ni otro framework.
4. Ejecuta primero `--dry-run`, muestra nombre, destino y propietario, y pide confirmación explícita antes de crear archivos o un remoto.
5. Tras confirmar, ejecuta el generador con `--type website`, `--name` y `--components web`.
6. Si GitHub CLI no está instalado o autenticado, informa y pregunta si se desea crear solo localmente con `--no-remote`.

El generador crea el esqueleto de estándares y metadatos; no configura framework ni dependencias web.