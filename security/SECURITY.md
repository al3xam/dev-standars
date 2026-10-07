# Seguridad y privacidad

**Estado:** borrador v0.1

Esta guía complementa la política de vulnerabilidades del README y aplica a todos los proyectos. Los perfiles tecnológicos pueden añadir controles específicos.

## Secretos y configuración

- No guardar tokens, contraseñas, claves privadas ni credenciales en código, historial Git, logs, issues, capturas o documentación.
- Usar el almacén de secretos de la plataforma de despliegue o variables de entorno protegidas. Los secretos de CI deben configurarse en el almacén seguro del proveedor.
- Mantener archivos locales como `.env` fuera de Git. Si se necesita documentar la configuración, versionar un `.env.example` con valores ficticios y sin secretos.
- Separar configuración y credenciales de desarrollo, pruebas y producción. No usar credenciales ni datos reales de producción en entornos de desarrollo o pruebas.
- Si un secreto se expone, revocarlo o rotarlo de inmediato. Eliminarlo del último commit no basta si ya entró en el historial o fue compartido.

## Aplicaciones cliente

- Tratar aplicaciones web y móviles distribuidas como entornos no confiables: el código y los valores incluidos en el cliente pueden inspeccionarse.
- No incluir secretos privilegiados ni credenciales de servidor en aplicaciones React, iOS o Android. Las operaciones privilegiadas deben ejecutarse y autorizarse en el servidor.
- Usar almacenamiento seguro de la plataforma para credenciales de usuario cuando deban persistirse; no guardarlas en texto plano ni en registros.

## Autenticación, autorización y comunicaciones

- Aplicar el principio de mínimo privilegio y denegar por defecto cuando falte una decisión de autorización.
- Validar la autorización en el servidor para cada operación protegida; no confiar en que el cliente oculte controles.
- Usar mecanismos de autenticación y seguridad proporcionados por la plataforma o framework cuando sean adecuados.
- Proteger las comunicaciones de producción mediante TLS y no desactivar la validación de certificados para resolver errores de conexión.

## Datos personales

- Recoger solo los datos necesarios para una finalidad documentada.
- Documentar, cuando el proyecto trate datos personales, qué recoge, para qué, quién puede acceder y cuánto tiempo se conserva; definir también cómo se corrigen o eliminan.
- Usar datos sintéticos o anonimizados en desarrollo, pruebas, fixtures, demos y capturas.
- Evitar datos personales en logs. Si registrar un identificador es imprescindible para diagnosticar, minimizarlo y controlar su acceso y retención.
- Cada proyecto debe cumplir las obligaciones de privacidad y conservación que le sean aplicables.

## Dependencias y vulnerabilidades

- Mantener los archivos de bloqueo y revisar las alertas de dependencias con regularidad.
- Ejecutar análisis de dependencias y los controles de seguridad disponibles en CI antes de publicar.
- Una vulnerabilidad crítica bloquea la publicación sin excepciones. Una alta bloquea salvo que se documente que es falso positivo o no explotable, con justificación y fecha de revisión. Las demás se registran para seguimiento.
- Aplicar el proceso de excepciones de [GLOBAL.md](../GLOBAL.md); las obligaciones legales, contractuales y de las tiendas no pueden exceptuarse.

## Respuesta a incidentes

Si se descubre exposición de secretos, acceso no autorizado o una vulnerabilidad explotable:

1. Contener el incidente; revocar credenciales expuestas y limitar el acceso afectado.
2. Determinar el alcance y qué sistemas o datos pudieron verse afectados.
3. Corregir la causa, rotar credenciales relacionadas y comprobar que la corrección funciona.
4. Registrar el incidente, las acciones y las decisiones de seguimiento sin copiar secretos ni datos personales al informe.
5. Evaluar las obligaciones aplicables de notificación y comunicación.
