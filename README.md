# 🐶 Tienda Perritos - DevOps & CI/CD Pipeline

Este repositorio contiene la arquitectura de microservicios para la **Tienda de Perritos**, optimizada con las mejores prácticas de DevOps, incluyendo contenerización avanzada, flujos de CI/CD, y estrategias de despliegue en AWS EC2.

---

## 🏗 Arquitectura del Sistema

La plataforma está diseñada en 3 capas (Tier-3):

1. **Frontend**: SPA HTML/JS ligera servida mediante Nginx.
2. **Backend**: API RESTful construida en Node.js (Express) que expone endpoints `/api/productos`.
3. **Base de Datos**: MySQL 8.0 para persistencia transaccional.

---

## 🚀 Contenerización (Mejores Prácticas Implementadas)

Los `Dockerfile` de este proyecto han sido refactorizados buscando la máxima seguridad y eficiencia:

*   **Multi-stage Builds**: Separación de las etapas de construcción de dependencias y ejecución de producción (Frontend y Backend).
*   **Imágenes Ligeras**: Uso de `alpine` para minimizar la superficie de ataque y el tamaño final (`node:18-alpine` y `nginxinc/nginx-unprivileged:alpine`).
*   **Seguridad (Non-Root User)**: 
    *   Backend ejecuta bajo el usuario predefinido `node` en lugar de root.
    *   Frontend usa `nginx-unprivileged` corriendo en el puerto `8080` (en lugar del puerto 80 restringido a root).
*   **Auto-recuperación**: Directivas `HEALTHCHECK` integradas directamente a nivel Dockerfile para todos los servicios.

---

## 🐳 Despliegue Local (Docker Compose)

El archivo `docker-compose.yml` está preparado para levantar el ecosistema completo en modo desarrollo/testing.

### Características:
*   **Red dedicada**: `app-network` aísla los contenedores.
*   **Persistencia de datos**: `named volume` (`db_data`) garantiza que los datos de MySQL no se pierdan si se destruye el contenedor.
*   **Inyección de variables**: Uso de variables de entorno explícitas.
*   **Secuenciación estricta**: Uso de `depends_on` con `condition: service_healthy` asegura que el backend espere a la DB, y el frontend al backend.

### ¿Cómo ejecutarlo?
```bash
docker compose up -d --build
```
> El Frontend estará disponible en `http://localhost`, el Backend en `http://localhost:3001` y la BD en el `3306`.

---

## ⚙️ CI/CD y Amazon AWS

El proyecto incluye 3 flujos de trabajo independientes en `.github/workflows` que implementan:

*   **Trigger Específico**: Los despliegues se activan **únicamente** al hacer `push` a la rama `deploy`.
*   **Estrategia de Tagging**: Generación de tags dinámicos (`latest`, `v1`, `v1.0.0`) empujados hacia **Amazon ECR**.
*   **Despliegue Serverless-like a EC2**: A través de AWS Systems Manager (SSM), el runner ejecuta comandos seguros directamente en las instancias EC2 sin requerir abrir puertos SSH.

### 🛡 Consideraciones de Seguridad en AWS (Security Groups)

El despliegue asume la siguiente segmentación a nivel de red (AWS VPC Security Groups):
1.  **Frontend EC2**: Expone puerto 80 hacia `0.0.0.0/0` (Internet).
2.  **Backend EC2**: Expone puerto 3001 **solo** permitiendo tráfico entrante desde la Private IP / Security Group del Frontend.
3.  **Database EC2**: Expone puerto 3306 **solo** permitiendo tráfico desde la Private IP / Security Group del Backend.

---

## 🛠 Troubleshooting

*   **Frontend no conecta al backend en EC2**: Verifica que los secretos de GitHub `BACKEND_HOST` coincidan con la IP Privada real de tu EC2 del Backend.
*   **La base de datos pierde información**: No ejecutes `docker compose down -v`. Si usas `docker run` en EC2, asegúrate de utilizar `-v db_data:/var/lib/mysql`.
