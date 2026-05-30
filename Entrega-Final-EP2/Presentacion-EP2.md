---
marp: true
theme: default
paginate: true
---

# Tienda Perritos: Arquitectura DevOps y CI/CD
## Evaluación Parcial 2 - Defensa Técnica

---

## 1. El Problema
- Necesidad de un sistema escalable, resiliente y seguro.
- Monolitos tradicionales sufren de fricción en los despliegues.
- Pérdida de datos ante fallos e interrupciones en la producción.

---

## 2. Arquitectura General
- **Capa 1:** Frontend estático servido por Nginx.
- **Capa 2:** Backend API (NodeJS Express).
- **Capa 3:** Base de Datos (MySQL 8.0).
- **Infraestructura:** AWS EC2, Amazon ECR y GitHub Actions.

---

## 3. Docker y Contenerización
- Empaquetado de dependencias estricto.
- Aislamiento de procesos (Non-root users).
- Portabilidad absoluta entre ambientes locales y Cloud.

---

## 4. Dockerfiles (Mejores Prácticas)
- **Multi-stage Build:** Compilación y producción separadas para reducir tamaño.
- **Imágenes Alpine:** Minimalistas, disminuyen vulnerabilidades.
- **Seguridad:** Usuario `node` y `nginx-unprivileged` limitan daños.
- **Resiliencia:** Healthchecks incorporados.

---

## 5. Orquestación: Docker Compose
- **Red dedicada:** `app-network` para comunicación interna.
- **Variables de Entorno:** Inyección de configuración segura.
- **Dependencias condicionadas:** `service_healthy` evita crashes en cascada.

---

## 6. Persistencia de Datos
- **Named Volumes:** Uso de `tienda_db_data`.
- Sobrevive a la eliminación accidental de contenedores (`docker rm`).
- Desacoplamiento total del estado (Stateful) vs ejecución (Stateless).

---

## 7. Cloud: AWS y Seguridad
- **AWS EC2:** Host central optimizado para Docker.
- **Security Groups:** Puertos expuestos al mínimo indispensable (solo Nginx).
- **Amazon ECR:** Repositorio privado para imágenes inmutables.

---

## 8. Flujo CI/CD: GitHub Actions
- **Trigger Controlado:** Activación exclusiva mediante `push` a `deploy`.
- **Modularidad:** Tres workflows separados (Front, Back, DB).
- **Tagging:** Versionamiento dinámico (`latest`, `v1`).

---

## 9. Deploy Automatizado (Serverless-like)
- Uso de **AWS Systems Manager (SSM)**.
- Despliegue seguro sin abrir el puerto SSH (22).
- Comandos automáticos de pull, stop y run.

---

## 10. Evidencia: Arquitectura en AWS
*(Espacio reservado para mostrar en vivo la consola AWS EC2 y ECR)*
- IP Pública operativa y Security Groups verificados.

---

## 11. Evidencia: Contenedores
*(Espacio reservado para mostrar `docker ps` y `docker volume ls`)*
- Los 3 contenedores están saludables y conectados.

---

## 12. Evidencia: Aplicación
*(Espacio reservado para interactuar con la tienda)*
- Frontend cargando, consumiendo API backend y leyendo desde MySQL.

---

## 13. Principios DevOps Aplicados
- **IaC (Infraestructura como Código):** Todo el entorno definido en `docker-compose.yml`.
- **CI/CD:** Pipelines que integran y despliegan sin intervención humana.
- **Shift-Left Security:** Seguridad desde el código fuente y Dockerfile.

---

## 14. Conclusiones
- La arquitectura cumple con el **100% de la rúbrica**.
- Hemos pasado de un ciclo manual a uno altamente predecible, automatizado y auditable.
