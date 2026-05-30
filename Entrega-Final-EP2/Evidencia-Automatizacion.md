# Evidencia de Automatización CI/CD - Tienda Perritos

Este documento presenta la trazabilidad completa del ciclo de vida del código desde la máquina local hasta la infraestructura en AWS, demostrando un flujo DevOps maduro.

## Flujo Paso a Paso de Automatización

### 1. Desarrollo Local y Versionamiento
El ciclo comienza cuando el desarrollador completa una funcionalidad o mejora en el código (ej. actualizando `backend/server.js`).
1. El código se valida localmente usando Docker Compose (`docker-compose up -d --build`).
2. Se realiza el commit del código.
3. **Trigger de Automatización:** Al ejecutar `git push origin deploy`, GitHub detecta el cambio e inicia el pipeline.

### 2. Integración Continua (CI) en GitHub Actions
El archivo `.github/workflows/cicd-tienda-backend.yml` (y sus homólogos) es interpretado por GitHub.
1. Se provisiona un `Runner` (Ubuntu-latest).
2. Se autentica en Amazon AWS usando las credenciales seguras (Secrets).
3. Se loguea en Amazon ECR (`aws ecr get-login-password`).
4. **Build Docker:** Se ejecuta el `docker build` en modalidad `Multi-stage`. Aquí se aíslan las dependencias de compilación y se genera una imagen limpia.
5. **Tagging:** Se etiqueta la imagen dinámicamente (`latest` y versión del commit).

### 3. Entrega Continua (CD) hacia Amazon ECR
Una vez compilada, la imagen es transmitida a nuestro repositorio de contenedores en AWS.
1. Se ejecuta `docker push 471112880379.dkr.ecr.us-east-1.amazonaws.com/tienda-backend:latest`.
2. ECR registra la nueva imagen, escaneando vulnerabilidades de capa base si está habilitado.

### 4. Despliegue Automatizado en Amazon EC2
Aquí es donde ocurre la mayor innovación arquitectónica del proyecto: **Serverless-like Execution** a través de AWS SSM (Systems Manager).
1. El Runner de GitHub ejecuta el comando `aws ssm send-command`.
2. Este comando se comunica internamente con el Agente de SSM alojado dentro de nuestra instancia EC2 (`i-02b10fe2f2eaed832`).
3. El Agente de la EC2 ejecuta un bloque de scripts sin necesidad de abrir puertos (como SSH 22):
   ```bash
   aws ecr get-login-password | docker login ...
   docker pull .../tienda-backend:latest
   docker stop tienda-backend || true
   docker rm tienda-backend || true
   docker run -d --name tienda-backend --network tienda-network ...
   ```
4. Los contenedores viejos son reemplazados sin downtime catastrófico y se unen a la red privada `tienda-network`.

## Resultados Finales (Evidencia)
Al finalizar el workflow (aprox. 1 minuto y 30 segundos), la aplicación queda expuesta a Internet en `http://54.196.115.197/`. Todo esto ocurre sin intervención humana, cumpliendo con el estándar oro de DevOps.

*(Consulta la carpeta `diagramas/` para ver el esquema visual de este flujo).*
