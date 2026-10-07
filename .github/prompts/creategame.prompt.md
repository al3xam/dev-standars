---
name: creategame
description: "Crear un proyecto de juego y elegir sus plataformas objetivo."
argument-hint: "Nombre y plataformas, por ejemplo iOS y Android"
agent: agent
---

Crea un proyecto de tipo `game` bajo `games/` usando el generador compartido.

1. Si faltan datos, pregunta el nombre del juego y las plataformas objetivo disponibles (`ios`, `android`). El nombre debe usar minúsculas y kebab-case y debe seleccionarse al menos una plataforma.
2. No preguntes la ruta: el generador calcula el destino bajo la raíz de desarrollo configurada. No preguntes la visibilidad: los repositorios siempre son privados. Usa el propietario de GitHub autenticado, salvo que el usuario indique una organización.
3. Localiza `scripts/create-project.sh` en el repositorio de estándares o `.dev-standards/scripts/create-project.sh` si está instalado. No inventes una tecnología o motor de juego.
4. Ejecuta primero `--dry-run`, muestra nombre, plataformas, destino y propietario, y pide confirmación explícita antes de crear archivos o un remoto.
5. Tras confirmar, ejecuta el generador con `--type game`, `--name` y `--components` con las plataformas seleccionadas.
6. Si GitHub CLI no está instalado o autenticado, informa y pregunta si se desea crear solo localmente con `--no-remote`.

El generador crea el esqueleto de estándares y metadatos; no instala un motor ni un framework.