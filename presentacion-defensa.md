# Guion de Defensa Técnica - Evaluación Parcial 2 DevOps

Este documento está diseñado para ser estudiado antes de la presentación y sirve como material de apoyo durante la defensa de 15 minutos.

## 1. Introducción (2 min)
*   **Apertura**: "Buenos días, profesor. Hoy presentaré la arquitectura DevOps automatizada para la plataforma 'Tienda Perritos'. El enfoque principal de este proyecto fue llevar una aplicación estándar de 3 capas hacia estándares de la industria usando contenedores seguros, persistencia resiliente y un pipeline de integración y entrega continua (CI/CD) completamente serverless (usando ECR y SSM)."
*   **Objetivo cumplido**: "Se lograron todos los puntos de la rúbrica, garantizando máxima seguridad (Non-Root), eficiencia (Multi-stage), persistencia de la data, y automatización condicional a la rama `deploy`."

## 2. Explicación de Dockerfiles (3 min)
*   **Backend**: "Para el backend en Node.js, apliqué un build **Multi-stage**. En una primera etapa temporal instalamos las dependencias. En la segunda etapa, que es la que va a producción, solo copiamos lo necesario. Lo más importante: usamos el usuario `node` nativo de la imagen para que la aplicación no corra como `root`, previniendo escalamiento de privilegios. También añadí un `HEALTHCHECK`."
*   **Frontend**: "El Frontend ahora utiliza `nginxinc/nginx-unprivileged:alpine`. Esto nos obligó a cambiar el puerto interno del 80 al `8080`, ya que los usuarios sin privilegios no pueden abrir puertos menores a 1024. Además, utilizamos un `template` de nginx que, al inyectarle la IP del backend como variable de entorno, permite que el contenedor sea dinámico en AWS sin hardcodear IPs en la imagen."
*   **Base de datos**: "Usamos la imagen oficial de MySQL 8, pero inyecté un `HEALTHCHECK` mediante `mysqladmin ping`. Esto es crucial para la orquestación."

## 3. Orquestación: Docker Compose (3 min)
*   "Generé un archivo `docker-compose.yml` que facilita el levantamiento local. Destaco 3 puntos:
    1.  **Red Privada**: Creé `app-network` para que los contenedores se descubran por su nombre sin exponerse a la máquina host internamente.
    2.  **Persistencia**: Definí el volumen `db_data` asociado a `/var/lib/mysql`. Gracias a esto, aunque el contenedor de BD se caiga, la data perdura.
    3.  **Dependencias Sanas**: No me limité a un `depends_on` normal; usé `condition: service_healthy`. Así, el Backend no arranca hasta que el ping de MySQL devuelve OK, evitando crashes en cascada."

## 4. Pipeline de CI/CD y Registro (4 min)
*   **Trigger**: "Modifiqué los GitHub Actions para que solo se activen ante un evento `push` en la rama `deploy` y solo si hubo cambios en su respectiva carpeta, optimizando los minutos de ejecución gratuitos de GitHub."
*   **Registro**: "Enviamos la imagen a **Amazon ECR**. Configuré el pipeline para que genere **múltiples tags** (`latest`, `v1`, `v1.0.0`) asegurando un correcto versionamiento."
*   **Despliegue a EC2**: "Para el despliegue automático, utilizamos AWS SSM (`send-command`). Esto es una excelente práctica porque evita que tengamos que abrir el puerto SSH 22 en las instancias de AWS, el runner de GitHub manda el comando al agente de SSM de AWS internamente y despliega los nuevos contenedores."

## 5. Preguntas Frecuentes del Profesor y Respuestas (3 min)

> **Pregunta:** ¿Por qué utilizaste `multi-stage build` en el backend?
> **Respuesta Técnica:** "Para reducir el tamaño de la imagen final y mejorar la seguridad. Nos permite separar el entorno donde descargamos dependencias (que a veces requiere herramientas extra de compilación como python o gcc) de la imagen de producción, que se mantiene purgada y mínima."

> **Pregunta:** ¿Por qué no dejaste que el contenedor de Nginx corriera con el usuario root?
> **Respuesta Técnica:** "Es un principio de *least privilege*. Si existe una vulnerabilidad en Nginx o en nuestra app y un atacante logra ejecutar código, al no ser root, su capacidad de dañar el contenedor o intentar saltar al host (container breakout) es muchísimo menor."

> **Pregunta:** ¿Cuál es la diferencia entre un bind mount y un named volume, y por qué usaste named volume para la BD?
> **Respuesta Técnica:** "Un bind mount liga una ruta específica de la máquina host al contenedor. Es útil para código en desarrollo. Un **named volume**, en cambio, es gestionado completamente por Docker dentro de su área segura (`/var/lib/docker/volumes`). Lo elegí para la BD porque aísla la data de permisos de host, mejora el rendimiento (especialmente en macOS/Windows) y facilita los backups nativos de Docker."

> **Pregunta:** En AWS, ¿Cómo impides que un usuario acceda directo a tu Backend?
> **Respuesta Técnica:** "A través de **Security Groups** a nivel de la VPC. El EC2 del Backend no tiene permitido tráfico TCP en el puerto 3001 desde `0.0.0.0/0`. Solo acepto reglas de *Inbound* cuyo origen sea el Security Group atachado a la instancia del Frontend."

---

*Diagrama de Arquitectura sugerido (Dibujar o mostrar en presentación):*
`Usuario -> [EC2 Frontend (80) SG_Web] -> [EC2 Backend (3001) SG_App] -> [EC2 DB (3306) SG_DB]`
