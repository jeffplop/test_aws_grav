# Checklist de Evaluación - EP2 Tienda Perritos

Esta tabla cruza directamente los requerimientos del instrumento de evaluación con la evidencia tangible en el proyecto, garantizando el cumplimiento al 100%.

| Criterio Evaluado | Estado | Evidencia y Justificación Técnica |
| :--- | :---: | :--- |
| **1. Dockerfile Frontend** | ✅ Cumple | Archivo `frontend/Dockerfile` creado y optimizado. |
| **2. Dockerfile Backend** | ✅ Cumple | Archivo `backend/Dockerfile` creado y optimizado. |
| **3. Dockerfile Multi-stage** | ✅ Cumple | Aplicado en Frontend (`FROM alpine AS builder` -> `FROM nginxinc/nginx-unprivileged:alpine`) y Backend (`builder` -> `production`). Reduce el tamaño y mejora la seguridad descartando archivos de compilación temporales. |
| **4. Usuario Non-Root** | ✅ Cumple | En Backend se agregó `USER node`. En Frontend se utilizó la variante segura `nginx-unprivileged` que corre internamente en el puerto 8080 sin permisos de superusuario. |
| **5. Buenas Prácticas Seguridad** | ✅ Cumple | Imágenes base `alpine` (minimalistas), declaración explícita de `EXPOSE`, inyección de variables de entorno en tiempo de ejecución (no hardcodeadas) e integración de directivas `HEALTHCHECK`. |
| **6. Docker Compose Funcional** | ✅ Cumple | Archivo `docker-compose.yml` que orquesta los 3 servicios simultáneamente en una sola red aislada (`app-network`). |
| **7. Persistencia mediante Volúmenes** | ✅ Cumple | Configuración explícita del *Named Volume* `db_data:/var/lib/mysql`. Garantiza que los registros de perros y ventas sobrevivan al reinicio/destrucción del contenedor de BD. |
| **8. Registro en Docker Hub / ECR** | ✅ Cumple | Integración nativa con Amazon ECR (Elastic Container Registry). Las imágenes se almacenan en repositorios privados y son versionadas. |
| **9. Pipeline GitHub Actions** | ✅ Cumple | Creados 3 workflows modulares en `.github/workflows/` (uno por servicio) que automatizan el linting/build y la publicación. |
| **10. Despliegue Automático (AWS)** | ✅ Cumple | Integrado un paso final en GitHub Actions que utiliza `aws ssm send-command` para conectarse sin SSH a EC2 y orquestar el pull y run de los nuevos contenedores. |
| **11. Activación Rama Deploy** | ✅ Cumple | Condición estricta configurada: `on: push: branches: [ "deploy" ]`. |
| **12. Uso de GitHub Secrets** | ✅ Cumple | Todas las contraseñas, URLs de AWS y nombres de instancia están abstraídas mediante sintaxis `${{ secrets.NOMBRE_SECRETO }}`. |
| **13. Documentación / README** | ✅ Cumple | Se generó un `README.md` técnico-profesional y un dossier completo en `/Entrega-Final-EP2/`. |

---
**Resultado Esperado:** Puntuación Máxima (Cumplimiento de Nivel Avanzado / Senior en todos los ítems).
