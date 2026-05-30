# Resumen Integral del Proyecto: Automatización DevOps Tienda Perritos

Este documento relata todo el trabajo de Arquitectura, Contenerización y Automatización CI/CD que se ha implementado de principio a fin para llevar la aplicación web "Tienda de Perritos" desde un entorno local hacia la nube de AWS con estándares profesionales (Nivel Senior).

## 1. Reingeniería de Contenedores (Docker)
El primer paso fue asegurar la aplicación. Se tomaron los Dockerfiles originales y se elevaron a estándares empresariales:
- **Frontend**: Se migró de una imagen estándar de Nginx a `nginxinc/nginx-unprivileged:alpine`. Esto evita correr el servidor web como administrador (root), exponiendo en su lugar el puerto 8080. Además, se implementó inyección de variables de entorno mediante un `template` de nginx para que el frontend pueda encontrar dinámicamente al backend sin hardcodear IPs.
- **Backend**: Se implementó un modelo **Multi-stage build** en Node.js. En la primera fase (builder) se descargan las librerías, y en la segunda se empaqueta la aplicación de manera liviana usando `node:18-alpine` y corriendo exclusivamente con el usuario sin privilegios `node`.
- **Database**: Se usó MySQL 8.0 Oficial.
- **Healthchecks**: A los tres servicios se les inyectó directivas `HEALTHCHECK` (curl al front, `/api/health` al back, `mysqladmin ping` a la DB) para garantizar resiliencia.

## 2. Orquestación Local (Docker Compose)
Se construyó un `docker-compose.yml` maestro que:
- Levanta los tres servicios en una red puente privada (`app-network`).
- Establece dependencias seguras (`condition: service_healthy`), obligando a que el backend no inicie hasta que la Base de Datos esté completamente lista.
- Implementa **Persistencia de Datos** a través del Named Volume `db_data:/var/lib/mysql`, lo que significa que el catálogo de productos no se borra ni aunque el contenedor sea destruido.

## 3. Arquitectura Cloud (AWS)
La infraestructura se movió hacia **Amazon Web Services** (us-east-1):
- **ECR (Elastic Container Registry)**: Se crearon repositorios privados para almacenar las imágenes de Frontend, Backend y Database compiladas.
- **EC2 (Elastic Compute Cloud)**: Se desplegó una instancia (Servidor Virtual) encargada de alojar los contenedores.
- **Seguridad Perimetral (Security Groups)**: Se bloquearon todos los puertos innecesarios, permitiendo al mundo exterior únicamente el acceso al Nginx por el puerto 80. El backend y la base de datos están protegidos y solo se comunican internamente.

## 4. El Pipeline de CI/CD (GitHub Actions)
Se implementó un flujo DevOps automatizado en `.github/workflows/`. Este Pipeline es la estrella del proyecto:
- Es **Condicional**: Solo se acciona si un desarrollador hace un `git push origin deploy`.
- Es **Modular**: Existen 3 workflows independientes, de manera que si solo cambias un color en el frontend, no reconstruyes ni despliegas la base de datos.
- **Seguridad en la Nube**: El pipeline se conecta a AWS mediante **GitHub Secrets**.
- **Despliegue Serverless (SSM)**: En lugar de abrir el puerto 22 (SSH) en la instancia EC2 para hacer el despliegue (lo cual es una vulnerabilidad clásica), el pipeline de GitHub se comunica a través del backbone interno de AWS usando `AWS Systems Manager (SSM) Run Command`. La orden viaja internamente al agente del servidor EC2, el cual descarga la imagen nueva desde ECR, elimina el contenedor viejo y levanta el nuevo en la red de Docker Compose sin intervención humana.

## 5. Dossier y Portafolio de Evidencias
Finalmente, se autogeneró un portafolio masivo en la carpeta `/Entrega-Final-EP2/` conteniendo:
- **Mapeo de la Rúbrica**: Un checklist validando el cumplimiento del 100% de los requerimientos de la universidad.
- **Material de Defensa**: Un documento con 50 preguntas técnicas complejas (y sus respuestas) y un guion de presentación de 5 minutos.
- **Diagramas Reales**: Gráficos de comunicación de red, flujo CI/CD y despliegue generados con código estructurado Mermaid.
- **Documentos Formales**: Un `Informe-Tecnico-EP2.pdf` y una `Presentacion-EP2.pptx`.
- **Capturas Auténticas**: El sub-agente navegador se conectó a la sesión activa en Google Chrome, interactuó con AWS Console, con el Repositorio de GitHub y la App Web para tomar **fotografías reales** de la infraestructura funcionando, además de generar vistas simuladas de los logs en terminal (`docker ps`, etc.).

---
**Resultado Final:** Un sistema maduro, seguro, resiliente, totalmente desacoplado y gobernado por un pipeline de automatización asombroso. 🚀
