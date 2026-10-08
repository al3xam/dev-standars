---
name: updatestandards
description: "Comparar y actualizar los estándares instalados en un proyecto tras revisar el diff."
argument-hint: "Proyecto que quieres actualizar, si no es el actual"
agent: agent
---

Actualiza los estándares de un proyecto solo con revisión y consentimiento explícito.

1. Determina el proyecto actual por su `.dev-standards/project.yml`. Si se invoca desde el repositorio central o hay varios proyectos, lista los proyectos disponibles por manifiesto y pide seleccionar uno.
2. Localiza el actualizador en `.dev-standards/scripts/update-standards.py` o `scripts/update-standards.py` y ejecútalo sin `--apply` para obtener el diff. La fuente central usa su rama `main` y la versión SemVer de `templates/project.yml`.
3. Muestra la versión instalada y la candidata, los archivos que cambiarían y los conflictos de personalización. No modifiques ningún archivo durante esta fase.
4. Pide confirmación explícita para aplicar. Si el usuario la rechaza, no cambies nada.
5. Tras confirmación, vuelve a ejecutar el actualizador con `--apply`. Si detecta conflictos, no fuerces la actualización: presenta el diff y solicita una decisión.
6. Ejecuta las comprobaciones disponibles y presenta el diff final. No combines esta operación con cambios funcionales ni hagas commit o push automáticamente.

Si no se puede localizar una fuente de estándares fiable, no adivines ni sobrescribas la copia instalada: explica el bloqueo y solicita la información necesaria.