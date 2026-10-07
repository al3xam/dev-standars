---
name: editproject
description: "Elegir un proyecto existente, cargar su contexto y trabajar en una tarea concreta."
argument-hint: "Proyecto o cambio que quieres realizar"
agent: agent
---

Ayuda al usuario a trabajar en un proyecto existente sin cargar ni modificar uno equivocado.

1. Localiza proyectos buscando `.dev-standards/project.yml` bajo la raíz de desarrollo configurada o el workspace actual. Lee los manifiestos como YAML; no deduzcas el tipo solo por el nombre de la carpeta.
2. Si hay varios proyectos aplicables, presenta una lista con nombre, tipo, componentes y ruta y pide que el usuario elija. No preguntes la ruta si la raíz ya está configurada.
3. Lee el `AGENTS.md`, `CONTEXT.md`, README y documentación relevante del proyecto, además del perfil de estándares que le corresponda.
4. Compara la versión instalada en `.dev-standards/project.yml` con la versión disponible de los estándares. Si hay una actualización, ofrece continuar con la instalada, actualizar usando `/updatestandards` por separado o cancelar. Nunca mezcles la actualización con la tarea de código.
5. Pregunta el objetivo y los criterios de aceptación que falten. Divide trabajo independiente en agentes cuando reduzca el tiempo total y no cause conflictos de edición.
6. Antes de editar, resume alcance, criterios y archivos probables. Sigue el flujo de ramas del proyecto; no hagas push ni publiques sin confirmación explícita.
7. Al terminar, ejecuta las comprobaciones pertinentes, revisa el diff y resume cambios, resultados y cualquier criterio pendiente.