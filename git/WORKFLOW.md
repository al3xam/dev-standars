# Flujo de trabajo

**Estado:** borrador v0.1

Este flujo aplica a los proyectos personales. Los perfiles tecnológicos pueden añadir comprobaciones específicas; si existe una contradicción, se sigue la jerarquía de [GLOBAL.md](../GLOBAL.md).

## Una tarea está lista cuando

- Tiene un objetivo y criterios de aceptación verificables registrados en el issue o sistema de seguimiento.
- Se conoce el proyecto, tipo o componentes afectados y se han identificado dependencias relevantes.
- El alcance es suficientemente acotado para desarrollarlo y validarlo en una rama breve.
- No quedan decisiones previas sin resolver que impidan empezar.

## Desarrollo de una tarea

1. Crear una rama corta desde `develop`, con un prefijo según el tipo de trabajo: `feature/`, `fix/`, `chore/`, `docs/` o `test/`.
2. Incluir el identificador de la tarea en el nombre cuando exista, por ejemplo `feature/123-login-social`.
3. Mantener una tarea principal por rama; dividir tareas independientes en ramas separadas.
4. Consultar los requisitos globales y los perfiles aplicables antes de modificar el proyecto.
5. Ejecutar las comprobaciones pertinentes mientras se desarrolla, no solo antes de publicar.

## Uso de agentes

- Valorar la ejecución paralela cuando haya tareas independientes y la coordinación no cueste más que el tiempo ahorrado.
- Delegar cada parte con objetivo, alcance, archivos o interfaces relevantes y resultado esperado claros.
- Evitar que varios agentes modifiquen simultáneamente los mismos archivos o trabajen sobre decisiones aún abiertas.
- Mantener secuenciales las tareas dependientes. El agente coordinador integra el trabajo, revisa los resultados y ejecuta las comprobaciones finales.
- Los agentes no pueden rebajar requisitos ni aprobar excepciones; deben señalar conflictos al mantenedor.

## Commits y push

- Crear un commit local después de completar un cambio lógico y revisar que las comprobaciones pertinentes pasen. No esperar hasta terminar toda la tarea para guardar el trabajo.
- Mantener los commits acotados a la tarea y no incluir secretos, archivos temporales ni cambios generados que el proyecto no versiona.
- Hacer push de la rama de tarea después del primer cambio comprobado y al final de cada bloque de trabajo significativo, especialmente antes de pausar. No es necesario hacer push por cada edición pequeña.
- Usar el push para respaldar el trabajo y ejecutar CI en el remoto. Si CI falla, corregir la rama antes de integrarla.
- Integrar la rama de tarea en `develop` solo después de cumplir los criterios de terminado y tener CI en verde. Para proyectos individuales se recomienda usar un pull request para revisar el diff; no se requiere aprobación de otra persona.
- En GitHub, proteger `main` con las reglas disponibles para prohibir force-push y borrado de la rama. Verificar la configuración después de crear el repositorio remoto.
- Si el plan o la configuración de GitHub no permiten aplicar esas protecciones, informar que `main` no está protegido; no presentar la regla como aplicada.
- Evitar commits directos en `develop` y `main` y no reescribir su historial.
- Publicar en el remoto las ramas iniciales `main` y `develop` al crear el repositorio. Las etiquetas de release también se publican en el remoto.

## Una tarea está terminada cuando

- Cumple sus criterios de aceptación y no incluye cambios ajenos a su alcance.
- Pasan CI y las pruebas, análisis estático y verificaciones que exija el perfil del proyecto.
- Se actualiza la documentación afectada.
- No introduce secretos ni vulnerabilidades bloqueantes según el estándar global.
- El mantenedor realiza una revisión personal del diff. No se exige aprobación de otra persona en proyectos individuales.
- Se integra en `develop`; el merge no implica que ya esté publicada en producción.

## Ramas y releases

- `main` representa producción y debe corresponder a una versión publicada o lista para publicar.
- `develop` integra el trabajo destinado a la próxima versión y, cuando sea posible, alimenta un entorno de pruebas, una beta o builds internos.
- CI debe pasar antes de integrar cambios en `develop` o `main`.
- Preparar una release cuando el alcance previsto esté completo, las comprobaciones pasen, no existan vulnerabilidades bloqueantes y la candidata se haya validado en staging, beta o builds internos.
- Para publicar, actualizar la versión SemVer y las notas de cambios, integrar `develop` en `main` y crear una etiqueta de Git para el release.
- Usar una rama `release/*` solo si hace falta estabilizar una candidata mientras continúa el desarrollo; limitarla a correcciones de esa release.
- Las correcciones urgentes parten de `main`; tras publicarlas, integrar también los cambios en `develop`.
- Si no hay un entorno de pruebas, beta o builds internos, la rama `develop` separa el trabajo en curso, pero no demuestra que funcione en un entorno real.
