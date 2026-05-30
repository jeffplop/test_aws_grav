# INFOGRAFÍA DEVOPS: TIENDA PERRITOS

Una vista rápida a las prácticas ágiles y de operaciones en la Tienda Perritos.

## 🏗️ 1. Infraestructura como Código y Orquestación
- **Herramienta:** Docker Compose (`docker-compose.yml`)
- **Impacto:** Levantar 3 servidores, redes aisladas y almacenamiento de bases de datos con solo `1` comando (`docker compose up`).
- **Mejora:** Elimina la deriva de configuración. Lo que corre localmente, correrá igual en AWS.

## 🔒 2. Seguridad "Shift-Left"
- **Contenedores Non-Root:** El usuario `node` (NodeJS) y `nginx` (Nginx) corren sin privilegios de administrador.
- **Micro-imágenes:** `node:18-alpine` pesa menos de 200MB, frente a los >1GB de una imagen base completa, reduciendo librerías vulnerables (CVEs).
- **Red Aislada AWS:** Puertos ocultos a internet público salvo el Nginx frontend (puerto 80).

## 🚀 3. CI/CD Pipeline Totalmente Automatizado
- **Ramas Estrictas:** Solo un push a la rama `deploy` activa el flujo de valor.
- **Agentless Deployment:** En vez de abrir huecos de seguridad SSH (puerto 22), se usa Amazon Systems Manager (SSM) para enviar comandos a través del backbone interno de Amazon.

## 🔄 4. Resiliencia y Auto-Healing
- **Healthchecks Nativos:** Cada contenedor se verifica a sí mismo (Nginx hace ping a su puerto 8080, Backend hace ping a `/api/health`, MySQL hace ping usando `mysqladmin`).
- **Secuenciación Segura:** Backend no arranca hasta que DB devuelva "Estoy listo" (`condition: service_healthy`).
