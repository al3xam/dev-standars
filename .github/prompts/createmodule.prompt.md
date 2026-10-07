---
name: createmodule
description: "Crear un proyecto para un módulo PrestaShop y registrar sus decisiones de distribución."
argument-hint: "Nombre técnico y propósito del módulo"
agent: agent
---

Crea un proyecto de tipo `prestashop` usando el generador compartido.

1. Pregunta el nombre técnico del módulo en minúsculas y kebab-case, su nombre visible y un resumen de su propósito.
2. Pregunta si será para uso propio, distribución directa o PrestaShop Addons. Pregunta si necesita actualizaciones desde GitHub; si se publicará en Addons, indica que sus reglas de distribución deben comprobarse antes de elegir un updater. Las actualizaciones, si se habilitan, deben ser manuales y confirmadas por el administrador.
3. No preguntes la ruta: el generador calcula el destino bajo la raíz configurada. Los repositorios siempre son privados; usa el propietario autenticado salvo que se indique una organización.
4. Localiza `scripts/create-project.sh` en el repositorio de estándares o `.dev-standards/scripts/create-project.sh` si está instalado. Ejecuta primero `--dry-run`, muestra el resumen y pide confirmación explícita antes de crear.
5. Tras confirmar, ejecuta el generador con `--type prestashop` y `--name`.
6. Registra el propósito, PrestaShop 8.2 como versión mínima, distribución elegida y decisión de actualizaciones en `CONTEXT.md`. No afirmes que existe un módulo ejecutable si solo se creó el esqueleto general del proyecto.
7. Si GitHub CLI no está instalado o autenticado, informa y pregunta si se desea crear solo localmente con `--no-remote`.