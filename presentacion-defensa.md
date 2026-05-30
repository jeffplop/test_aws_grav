# Guion de Defensa Técnica - Proyecto Semestral DevOps

Este documento está diseñado para ser estudiado antes de la presentación y sirve como material de apoyo durante la defensa.

## 1. Introducción (2 min)
*   **Apertura**: "Buenos días, profesor. Hoy presentaré la arquitectura DevOps automatizada para el Proyecto Semestral. El enfoque principal fue llevar una aplicación hacia estándares reales de la industria usando microservicios en Java Spring Boot, frontend en React Vite, persistencia segura y un pipeline CI/CD de 3 ramas automatizadas a Amazon EC2 (vía SSM y ECR)."
*   **Objetivo cumplido**: "Se lograron todos los puntos de la rúbrica, garantizando máxima seguridad (usuarios Non-Root), eficiencia en la construcción (Multi-stage builds en Maven y Node) y automatización condicional en la rama `deploy`."

## 2. Explicación de Dockerfiles (3 min)
*   **Backend (Ventas y Despachos)**: "Para ambos backends en Java, apliqué un build **Multi-stage**. En la primera etapa usamos Maven para descargar dependencias y compilar el `.jar`. En la etapa final, usamos `eclipse-temurin:17-jre-alpine`, que es minúscula. Lo más crítico de seguridad: configuré el usuario `spring` para que la aplicación no corra como `root`, previniendo escalamiento de privilegios."
*   **Frontend**: "El Frontend (React Vite) se compila con Node 18, y los estáticos resultantes se sirven usando `nginxinc/nginx-unprivileged:alpine` en el puerto `8080`. Además, el Nginx fue configurado como Proxy Reverso inteligente: redirige internamente `/api/ventas/` y `/api/despachos/` hacia los contenedores backend. Esto elimina el problema de CORS y oculta los backends de Internet."
*   **Base de datos**: "Usamos MySQL 8, montando automáticamente un script `init.sql` para preparar el esquema desde el arranque."

## 3. Orquestación: Docker Compose (3 min)
*   "Generé un archivo `docker-compose.yml` que orquesta los 4 contenedores y se usa directo en AWS. Destaco 3 puntos:
    1.  **Red Privada**: Creé `app-network` para que Front, Backends y DB se descubran por nombre interno, sin usar IPs públicas.
    2.  **Persistencia**: Definí el volumen `tienda_db_data` asociado a `/var/lib/mysql`. La data perdura ante reinicios o destrucción del contenedor de BD.
    3.  **Dependencias Sanas**: Usé `condition: service_healthy` para que Ventas y Despachos no arranquen hasta que el ping de MySQL devuelve OK."

## 4. Pipeline de CI/CD y Registro (4 min)
*   **Modularidad**: "Creé **3 workflows separados** en GitHub Actions (Frontend, Ventas, Despachos). Si solo cambio el frontend, no reconstruyo el código en Java. Se disparan con `push` en la rama `deploy`."
*   **Seguridad**: "Toda credencial y URL está oculta en GitHub Secrets."
*   **Despliegue a EC2**: "Para el despliegue automático (CD), utilizamos AWS SSM (`send-command`). En lugar de abrir el puerto SSH 22, SSM ordena al agente dentro del EC2 inyectar las URLs de Amazon ECR como variables de entorno y ejecutar un `docker compose pull && docker compose up -d`. Totalmente automatizado y altamente seguro."

## 5. Preguntas Frecuentes del Profesor y Respuestas (3 min)

> **Pregunta:** ¿Por qué utilizaste `multi-stage build` en Java?
> **Respuesta Técnica:** "Para reducir drásticamente la imagen final. Separamos el entorno de construcción (que necesita Maven y JDK completo, pesando cientos de MBs) del entorno de ejecución (que solo requiere JRE ligero y pesa una fracción), logrando un despliegue veloz y reduciendo la superficie de ataque."

> **Pregunta:** ¿Por qué no dejaste que los contenedores de Spring Boot o Nginx corrieran con root?
> **Respuesta Técnica:** "Principio de *menor privilegio*. Si hay una vulnerabilidad (Zero Day) en Nginx o Java y el atacante ejecuta código, al no ser root, su capacidad para vulnerar el host EC2 (container breakout) es muchísimo menor."

> **Pregunta:** ¿Cómo logras que el frontend hable con dos backends sin abrir más puertos en EC2?
> **Respuesta Técnica:** "A través de un Proxy Inverso en Nginx (`default.conf.template`). El frontend (React) hace peticiones a su propio dominio (`/api/ventas`). Nginx intercepta esto en el puerto interno 8080 y lo envía por la red privada de Docker (`app-network`) al contenedor `backend-ventas:8080`. Todo es transparente para AWS."

> **Pregunta:** Si tus 4 contenedores están en el `docker-compose.yml`, ¿Cómo configuras las instancias EC2 en GitHub Actions?
> **Respuesta Técnica:** "Coloco exactamente el mismo ID de instancia (ej. `i-0abcdef`) en las variables `EC2_FRONTEND_INSTANCE_ID`, `EC2_BACKEND_INSTANCE_ID` y `EC2_DB_INSTANCE_ID` en los Secrets de GitHub. Así los 3 pipelines ejecutan los comandos SSM apuntando al mismo servidor, asegurando que todos los microservicios se monten en el mismo entorno y se conecten exitosamente a través de `app-network`."

---

*Diagrama de Arquitectura sugerido:*
`[Usuario] --> EC2:80 --> [Nginx Frontend:8080] --> Proxy a [Backend Ventas:8080] y [Backend Despachos:8081] --> [MySQL:3306]`
