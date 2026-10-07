---
name: updatestandards
description: "Comparar y actualizar los estándares instalados en un proyecto tras revisar el diff."
argument-hint: "Proyecto que quieres actualizar, si no es el actual"
agent: agent
---

Actualiza los estándares de un proyecto solo con revisión y consentimiento explícito.

1. Determina el proyecto actual por su `.dev-standards/project.yml`. Si se invoca desde el repositorio central o hay varios proyectos, lista los proyectos disponibles por manifiesto y pide seleccionar uno.
2. Localiza la fuente central de estándares y compara su `templates/project.yml` con la versión instalada. Explica qué perfiles y documentos aplican al tipo y componentes del proyecto.
3. Muestra la versión instalada y la candidata, prepara un diff legible y señala personalizaciones o conflictos. No modifiques ningún archivo durante esta fase.
4. Pide confirmación explícita para aplicar la actualización. Si el usuario la rechaza, no cambies nada.
5. Tras confirmación, actualiza solo los estándares aplicables y el campo `standards.version`; preserva archivos de producto y personalizaciones ajenas a los estándares.
6. Ejecuta las comprobaciones disponibles y presenta el diff final. No combines esta operación con cambios funcionales ni hagas push automáticamente.

Si no se puede localizar una fuente de estándares fiable, no adivines ni sobrescribas la copia instalada: explica el bloqueo y solicita la información necesaria.