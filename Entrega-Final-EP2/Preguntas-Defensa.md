# Banco de Preguntas y Respuestas para Defensa Técnica - EP2

Este documento contiene 50 posibles preguntas que un docente podría realizar sobre la arquitectura, las decisiones técnicas y las herramientas utilizadas en el proyecto.

## DOCKER Y CONTENEDORES (1-10)

1. **¿Qué es Docker y qué problema resuelve?**
   *Docker es una plataforma de contenerización que empaqueta una aplicación y sus dependencias en un entorno aislado llamado contenedor, resolviendo el problema de "en mi máquina sí funciona" asegurando consistencia entre entornos.*

2. **¿Qué es un Dockerfile?**
   *Es un archivo de texto con una serie de instrucciones (receta) que Docker utiliza para ensamblar automáticamente una imagen.*

3. **¿Por qué usaste `Multi-stage build` en tus Dockerfiles?**
   *Para reducir el tamaño final de las imágenes y mejorar la seguridad. En una etapa se instalan las dependencias pesadas (builder) y en otra más limpia se copia solo lo compilado o necesario para correr en producción, sin arrastrar cachés ni herramientas de compilación.*

4. **¿Qué significa correr un contenedor con usuario `non-root`?**
   *Significa que el proceso principal dentro del contenedor no tiene permisos de superadministrador. Si un atacante vulnera la aplicación, sus permisos estarán muy limitados y no podrá escalar privilegios fácilmente hacia el host.*

5. **¿Cómo implementaste el usuario no-root en el Frontend?**
   *Utilizando la imagen base `nginxinc/nginx-unprivileged:alpine`, la cual está configurada para correr con el usuario `nginx` en lugar de root, y por lo tanto expone el puerto 8080 en vez del puerto privilegiado 80.*

6. **¿Qué hace la directiva `HEALTHCHECK`?**
   *Permite a Docker saber si el contenedor no solo está "corriendo", sino si la aplicación dentro de él está lista y sana para recibir tráfico.*

7. **¿Qué es una imagen `alpine` y por qué la elegiste?**
   *Es una distribución de Linux extremadamente ligera (aprox. 5MB). La elegí porque reduce drásticamente el tamaño de la imagen final, acelerando los tiempos de pull/push en CI/CD y reduciendo la superficie de ataque (menos paquetes instalados = menos vulnerabilidades).*

8. **¿Cuál es la diferencia entre una Imagen y un Contenedor?**
   *Una imagen es un archivo estático de solo lectura (la plantilla o clase), mientras que un contenedor es la instancia en ejecución (el objeto vivo) de esa imagen.*

9. **¿Qué es la directiva `EXPOSE`?**
   *Es una directiva puramente informativa en el Dockerfile que documenta en qué puerto está escuchando el servicio internamente, aunque no publica el puerto hacia el host por sí sola.*

10. **¿Cómo pasas variables dinámicas a tu Frontend en Nginx que es estático?**
    *Usé la funcionalidad de plantillas (templates) de la imagen oficial de Nginx. Se copia un archivo `default.conf.template` y al iniciar el contenedor, el script `envsubst` reemplaza las variables de entorno (ej. `$BACKEND_HOST`) por sus valores reales antes de arrancar el servidor.*

## DOCKER COMPOSE Y ORQUESTACIÓN (11-20)

11. **¿Qué es Docker Compose y en qué se diferencia de un Dockerfile?**
    *Mientras el Dockerfile define cómo construir un solo contenedor, Docker Compose (`docker-compose.yml`) define y orquesta cómo se comportan y comunican múltiples contenedores en conjunto como una aplicación completa.*

12. **¿Qué es una Docker Network y qué tipo usaste?**
    *Es una red virtual que permite a los contenedores comunicarse entre sí. Usé una red de tipo `bridge` definida por el usuario (`app-network`).*

13. **¿Por qué los contenedores se comunican por nombre (ej. `tienda-db`) en lugar de por IP?**
    *Porque las redes bridge creadas por el usuario en Docker incluyen resolución de DNS interno (DNS Service Discovery automático). Las IPs pueden cambiar si un contenedor se reinicia, el nombre no.*

14. **¿Para qué sirve `depends_on`?**
    *Define el orden de inicio de los servicios. En este caso garantiza que `db` inicie antes que `backend`, y `backend` antes que `frontend`.*

15. **¿Por qué agregaste `condition: service_healthy` al `depends_on`?**
    *Si solo se usa `depends_on`, Docker arranca el backend apenas el contenedor de la BD se enciende. Pero MySQL tarda unos segundos en aceptar conexiones. `service_healthy` obliga a esperar hasta que el `HEALTHCHECK` de MySQL responda OK.*

16. **¿Qué son los Volumes en Docker?**
    *Son mecanismos para persistir los datos generados y utilizados por los contenedores, almacenándolos fuera del ciclo de vida efímero del contenedor.*

17. **¿Cuál es la diferencia entre un Bind Mount y un Named Volume?**
    *Un Bind Mount enlaza una ruta específica del sistema host (ej. `/home/user/app`) al contenedor, útil para desarrollo. Un Named Volume es un espacio administrado 100% por Docker (ej. `db_data`), más seguro, eficiente y portátil para bases de datos.*

18. **¿Dónde vive físicamente la data de tu base de datos?**
    *En el host, dentro de la ruta `/var/lib/docker/volumes/tienda_db_data/_data` (en Linux).*

19. **¿Qué hace el comando `docker compose down -v`?**
    *Detiene los contenedores, remueve la red, los contenedores y **destruye los volúmenes asociados** (perdiendo la persistencia de datos).*

20. **¿Es buena práctica usar Docker Compose en producción?**
    *Para arquitecturas en un solo servidor (Single-Node) es aceptable y común. Para arquitecturas distribuidas complejas es mejor orquestadores robustos como Kubernetes o ECS.*

## AWS (21-30)

21. **¿Qué es EC2?**
    *Elastic Compute Cloud. Son máquinas virtuales escalables en la nube de AWS.*

22. **¿Qué es un Security Group?**
    *Es un firewall virtual a nivel de instancia que controla el tráfico entrante (inbound) y saliente (outbound) mediante reglas.*

23. **¿Por qué bloqueaste el puerto 3001 del Backend al mundo?**
    *Por seguridad (Defensa en profundidad). El cliente interactúa con el Frontend (Nginx), y es Nginx quien debe comunicarse con el Backend. No hay necesidad de que el Backend esté expuesto a Internet directamente.*

24. **¿Qué es Amazon ECR?**
    *Elastic Container Registry. Es un repositorio de imágenes Docker privado y administrado de AWS, equivalente a DockerHub pero integrado con el ecosistema de AWS.*

25. **¿Qué significa desplegar con AWS SSM en lugar de SSH?**
    *SSM (Systems Manager) usa un agente instalado en el EC2 que permite enviar comandos (Run Command) remotamente sin abrir puertos (como el 22 para SSH). Mejora enormemente la seguridad.*

26. **¿Qué es el IAM Instance Profile (`LabInstanceProfile`)?**
    *Es un rol de IAM (Identity and Access Management) adjuntado a la instancia EC2 que le otorga permisos temporales para llamar a otros servicios de AWS, como por ejemplo conectarse a ECR o S3 sin requerir credenciales hardcodeadas en el servidor.*

27. **¿Qué es S3 y cómo podría ayudar en CI/CD?**
    *Simple Storage Service es almacenamiento de objetos. Puede usarse para alojar la web estática (Frontend) o guardar artefactos de compilación (.zip o imágenes de respaldo) de forma muy barata.*

28. **¿Por qué la IP de EC2 puede cambiar y cómo lo evitas?**
    *La IP Pública estándar es efímera y cambia al detener/iniciar la instancia. Se evita asociando una Elastic IP (Dirección IP estática).*

29. **¿Qué es un VPC?**
    *Virtual Private Cloud. Es una red virtual privada aislada lógicamente en la nube de AWS donde residen nuestras instancias.*

30. **¿Cómo podrías hacer esta arquitectura altamente disponible?**
    *Colocando un Application Load Balancer (ALB) al frente, distribuyendo instancias EC2 en múltiples Availability Zones (Zonas de Disponibilidad) y usando un Auto Scaling Group.*

## GITHUB ACTIONS Y CI/CD (31-40)

31. **¿Qué significa CI/CD?**
    *Integración Continua (Continuous Integration) y Entrega/Despliegue Continuo (Continuous Deployment).*

32. **¿Qué detona el flujo en tu pipeline?**
    *Un evento `push` realizado específicamente en la rama llamada `deploy`.*

33. **¿Por qué creaste 3 workflows diferentes en vez de 1 solo?**
    *Para lograr modularidad. Si modifico algo en el frontend, solo se compila y despliega el frontend, ahorrando minutos de ejecución y acelerando el feedback.*

34. **¿Qué son los GitHub Secrets?**
    *Son variables de entorno encriptadas que permiten almacenar credenciales o tokens sensibles (como claves de AWS) sin exponerlas en el código fuente.*

35. **¿Por qué se taguean las imágenes como `latest` y con un `SHA` o versión (ej `v1`)?**
    *El tag `latest` es por convención la última versión disponible, pero usar tags inmutables (como un hash de git o versión `v1`) es necesario para poder hacer *rollback* a una versión específica si algo falla.*

36. **¿Qué hace el comando `aws ecr get-login-password` en el action?**
    *Obtiene un token de autenticación temporal de 12 horas desde AWS IAM y se lo pasa a `docker login` para poder subir las imágenes a nuestro ECR privado.*

37. **¿Qué es un `Runner` en GitHub Actions?**
    *Es el servidor que ejecuta los pasos definidos en tu archivo YML. Usamos `ubuntu-latest` que es una máquina virtual hospedada por GitHub con Docker preinstalado.*

38. **¿Cómo garantizas que el despliegue no falle si hay contenedores viejos?**
    *El comando de SSM incluye `docker rm -f <nombre_contenedor> || true`, lo que fuerza el borrado de los contenedores si existen, y con el `|| true` evita que el comando entero falle si los contenedores no estaban creados.*

39. **¿Qué significa la palabra clave `needs` en GitHub Actions?**
    *Indica que un Job depende de la ejecución exitosa de otro Job previo (creando una secuencia en vez de ejecución paralela).*

40. **Si GitHub Actions se cae, ¿qué alternativa usarías?**
    *Podría usar GitLab CI, Jenkins, AWS CodePipeline o Bitbucket Pipelines.*

## DEVOPS Y MEJORES PRÁCTICAS (41-50)

41. **¿Qué es la cultura DevOps?**
    *Es la integración y colaboración entre desarrollo (Dev) y operaciones (Ops) buscando automatización, monitoreo, fiabilidad y entregas de software más rápidas y de calidad.*

42. **¿Qué es Infraestructura como Código (IaC)?**
    *Es el proceso de gestionar y aprovisionar infraestructura a través de código (archivos de definición como Terraform o AWS CloudFormation) en lugar de procesos manuales.*

43. **¿Tu `docker-compose.yml` califica como IaC?**
    *Sí, califica como configuración como código o infraestructura a nivel local/contenedor, ya que define la topología de red, almacenamiento y servicios en formato declarativo (YAML).*

44. **¿Qué es el principio de "Idempotencia" en despliegues?**
    *Significa que ejecutar un script de despliegue 1 vez o 100 veces seguidas debe dar el mismo resultado sin romper el sistema. (Ej: Nuestro script que destruye y recrea la red y los contenedores de forma predecible).*

45. **¿Por qué no hardcodeaste `admin123` directamente en el Dockerfile?**
    *Por seguridad. Los secretos nunca deben ir en el código, ni siquiera en el Dockerfile porque quedan registrados en el historial de capas de la imagen. Se deben inyectar en tiempo de ejecución (ej. vía variables en Docker Compose o Secrets Manager).*

46. **¿Cómo monitorearías tu aplicación en AWS?**
    *Usaría Amazon CloudWatch para métricas de CPU/Memoria de las instancias EC2 y configuraría alarmas.*

47. **¿Qué es el "Shift-left" en DevOps?**
    *Significa mover pruebas, revisiones de código y análisis de seguridad hacia las etapas más tempranas del ciclo de desarrollo, evitando detectar errores cuando ya estamos en producción.*

48. **¿Qué significa que tus contenedores sean "Efímeros"?**
    *Significa que se pueden destruir, reemplazar y escalar rápidamente sin perder información, ya que el estado (la base de datos) está externalizado en un volumen.*

49. **Menciona 3 métricas DORA importantes.**
    *1. Lead Time for Changes (Tiempo para cambios), 2. Deployment Frequency (Frecuencia de despliegues), 3. Mean Time to Restore (Tiempo medio de restauración).*

50. **Si hoy tuvieras que escalar la BD, ¿qué harías?**
    *La migraría desde el contenedor EC2 hacia un servicio gestionado por AWS llamado Amazon RDS (Relational Database Service), el cual automatiza backups, replicación y escalabilidad.*
