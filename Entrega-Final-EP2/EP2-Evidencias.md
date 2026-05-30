# Dossier de Evidencias - Evaluación Parcial 2 (Tienda Perritos)

## 1. Resumen Ejecutivo
Este documento presenta la evidencia técnica verificable de la implementación de la Evaluación Parcial 2 de DevOps. El proyecto consiste en una arquitectura de microservicios de 3 capas (Frontend, Backend, Base de Datos) automatizada y contenerizada bajo las mejores prácticas de la industria, y desplegada en la nube de Amazon Web Services (AWS).

## 2. Arquitectura Implementada y Tecnologías
* **Frontend**: SPA estática servida por Nginx (Unprivileged, Alpine).
* **Backend**: Node.js (Express) para API RESTful.
* **Base de Datos**: MySQL 8.0 Oficial.
* **Contenedores**: Docker y Docker Compose v2.
* **Infraestructura Cloud**: AWS EC2 (Ubuntu/Amazon Linux), Amazon ECR, AWS SSM.
* **Automatización CI/CD**: GitHub Actions con flujos modulares y dependientes.

## 3. Checklist de Rúbrica y Cumplimiento

| Criterio de Rúbrica | Estado | Evidencia / Ubicación |
| :--- | :---: | :--- |
| **Dockerfile Frontend/Backend** | ✅ | `frontend/Dockerfile`, `backend/Dockerfile` |
| **Dockerfile Multi-stage** | ✅ | Aplicado en Frontend (`builder` -> `nginx`) y Backend (`builder` -> `node`). |
| **Usuario Non-Root** | ✅ | Backend usa `USER node`. Frontend usa `nginxinc/nginx-unprivileged`. |
| **Seguridad (Buenas Prácticas)** | ✅ | Uso de imágenes `alpine`, chown restringido, sin puerto 80 nativo en Nginx. |
| **Docker Compose Funcional** | ✅ | `docker-compose.yml` central. |
| **Persistencia de Volúmenes** | ✅ | Volumen `db_data` asociado a `/var/lib/mysql`. |
| **Publicación ECR/DockerHub** | ✅ | Imágenes tageadas como `latest` y pusheadas a Amazon ECR remoto. |
| **Pipeline CI/CD (GitHub Actions)** | ✅ | `.github/workflows/*.yml` configurados. |
| **Despliegue Automático (AWS)** | ✅ | Uso de `aws ssm send-command` para actualizar contenedores remotamente. |
| **Activación Rama Deploy** | ✅ | `on: push: branches: [ "deploy" ]` en todos los flujos. |
| **Uso de Secrets** | ✅ | Configuración inyectada vía `${{ secrets.* }}`. |
| **Documentación** | ✅ | `README.md` técnico + Presentación de defensa generada. |

## 4. Evidencias Docker

### 4.1. Construcción de Imágenes
El proceso `multi-stage` ha optimizado el tamaño de las imágenes drásticamente.
*(Ver captura en `evidencias/screenshots/docker_images.png` o equivalente)*

### 4.2. Ejecución y Persistencia
Todos los contenedores se ejecutan tras una validación de `healthcheck`.
```bash
$ docker volume ls
DRIVER    VOLUME NAME
local     tienda_db_data
```

## 5. Evidencias AWS
La infraestructura se ha aprovisionado en la región `us-east-1` utilizando el perfil académico.
* **EC2 Instance**: `i-02b10fe2f2eaed832` (`ec2-docker-lab`)
* **ECR Registry**: `471112880379.dkr.ecr.us-east-1.amazonaws.com`

## 6. Evidencias Integración (Frontend -> Backend -> DB)
Se ha demostrado mediante pruebas de caja negra a la IP pública:
`curl http://54.196.115.197/api/productos`
**Resultado**: Retorna JSON con catálogo, validando la cadena completa de red de Docker Compose `app-network`.
