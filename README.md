# 🚀 Proyecto Semestral DevOps - Sistema de Gestión de Despachos

Este repositorio contiene la arquitectura de microservicios para el **Sistema de Gestión de Despachos**, diseñada con estándares de la industria y las mejores prácticas de DevOps, incluyendo contenerización avanzada (Docker), automatización CI/CD (GitHub Actions), y orquestación dinámica en la nube de AWS.

---

## 🏗 Arquitectura de 4 Microservicios (Tier-4)

La plataforma ha dejado atrás arquitecturas monolíticas para abrazar un ecosistema distribuido y escalable:

1. **Frontend (React Vite)**: Aplicación SPA servida a través de **Nginx Unprivileged**. Este servidor actúa como Proxy Reverso para evitar exponer los backends a Internet.
2. **Backend Ventas (Java Spring Boot)**: API REST en el puerto interno `8080` que gestiona la lógica de órdenes de compra.
3. **Backend Despachos (Java Spring Boot)**: API REST en el puerto interno `8081` que gestiona la logística y estados de entrega.
4. **Base de Datos (MySQL 8.0)**: Base de datos relacional para persistencia transaccional centralizada.

---

## 🚀 Contenerización Segura e Inteligente

Los 4 `Dockerfile` de este proyecto han sido refactorizados buscando la máxima seguridad (DevSecOps) y eficiencia:

*   **Multi-stage Builds**: 
    *   **Java**: Primera etapa usa `maven` para compilar el código. Segunda etapa usa un `jre` minúsculo (`eclipse-temurin:17-jre-alpine`).
    *   **React**: Primera etapa usa `node:18` para transpilar Vite. Segunda etapa usa `nginx` para servir los estáticos.
*   **Imágenes Ligeras**: Reducción drástica del tamaño final de imagen usando arquitecturas `alpine`.
*   **Seguridad Estricta (Non-Root User)**: 
    *   Los microservicios de Spring Boot se ejecutan bajo el usuario sin privilegios `spring`.
    *   El Frontend usa `nginx-unprivileged` corriendo en el puerto seguro `8080` (en lugar del puerto 80 restringido a root).
*   **Auto-recuperación (Healthchecks)**: Comprobaciones de salud integradas (Nginx, curl, y `mysqladmin ping`).

---

## 🐳 Despliegue y Orquestación (Docker Compose)

El archivo `docker-compose.yml` maestro orquesta todo el ecosistema de red.

### Características implementadas:
*   **Red dedicada**: `app-network` aísla y comunica todos los contenedores mediante DNS interno. El frontend enruta mágicamente a `/api/ventas/` usando Nginx `proxy_pass`.
*   **Persistencia de datos**: El `named volume` (`tienda_db_data:/var/lib/mysql`) garantiza que las bases de datos de despachos sobrevivan destrucciones de contenedores.
*   **Secuenciación de arranque**: Uso de `depends_on` con `condition: service_healthy` asegura que los microservicios de Java no se inicien hasta que el motor MySQL responda al ping.
*   **Autoconfiguración DB**: El contenedor de BD corre un `init.sql` automático para preparar las tablas.

### ¿Cómo ejecutarlo localmente?
```bash
docker compose up -d --build
```
> El Frontend estará disponible en tu navegador en `http://localhost`. Todo el tráfico de las APIs será manejado internamente por el servidor Nginx, sin necesidad de conectarse directo al Backend.

---

## ⚙️ Integración y Entrega Continua (AWS + GitHub Actions)

El proyecto incluye flujos de automatización masiva en `.github/workflows`:

*   **Pipelines Desacoplados**: Existen flujos de despliegue separados. Si modificas el Frontend, GitHub *solamente* reconstruye y despliega el Frontend sin reiniciar los backends.
*   **Integración ECR**: Generación de etiquetas dinámicas (`latest`, `ventas-latest`, `despachos-latest`) y publicación privada en **Amazon Elastic Container Registry**.
*   **Despliegue Serverless-like a EC2**: A través de AWS Systems Manager (SSM), el runner de GitHub inyecta variables y ejecuta los comandos `docker compose pull` directamente en tu instancia EC2, sin necesidad de abrir el puerto SSH 22.

### 🛡 Configuración requerida en GitHub Secrets
Para que CI/CD funcione, en tu repositorio debes configurar las credenciales de Amazon Web Services (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`) y las URLs de tus repositorios ECR (`ECR_REPO_URL_FRONTEND`, `ECR_REPO_URL_BACKEND`, `ECR_REPO_URL_DB`). Para que todos los contenedores conversen en la misma red, asigna el mismo ID de servidor EC2 a las 3 variables de EC2.
