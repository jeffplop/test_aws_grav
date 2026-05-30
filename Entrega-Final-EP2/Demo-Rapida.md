# Guion de Demostración en Vivo (5 Minutos) - Tienda Perritos EP2

Este guion está cronometrado para demostrar el funcionamiento completo y sin fallos técnicos de la arquitectura en menos de 5 minutos frente al docente.

## Minuto 0:00 - 1:00 | 1. Presentación de AWS y EC2
*   **Abre la consola de AWS.**
*   Ve a **EC2 > Instancias**.
*   **Di:** *"Profesor, aquí tenemos nuestra instancia aprovisionada en la región `us-east-1`. Esta instancia está bajo el Security Group correspondiente que limita el acceso. Noten la IP pública `54.196.115.197`."*
*   Ve a **ECR**.
*   **Di:** *"Aquí están nuestros tres repositorios privados donde las GitHub Actions publican las imágenes Docker de forma automatizada."*

## Minuto 1:00 - 2:00 | 2. Demostración de CI/CD (GitHub Actions)
*   **Abre tu repositorio en GitHub > Actions.**
*   **Di:** *"Aquí tenemos los 3 workflows modulares. Si vemos el último despliegue exitoso (haz clic en uno), veremos cómo se integra el código, se construyen las imágenes en etapas (Multi-stage), se suben a ECR y finalmente se manda una orden serverless vía AWS SSM a nuestra instancia EC2 para que actualice los contenedores sin necesidad de abrir el puerto SSH 22."*
*   *(Opcional: muestra rápidamente el código del workflow en `.github/workflows/cicd-tienda-backend.yml`).*

## Minuto 2:00 - 3:00 | 3. Demostración de la Aplicación Front y Back
*   **Abre una nueva pestaña del navegador y entra a: `http://54.196.115.197/`**
*   **Di:** *"Esta es la Tienda de Perritos. El frontend estático está siendo servido por un contenedor Nginx seguro que no usa usuario root (Non-root, puerto 8080 interno). Podemos ver los productos listados correctamente."*
*   **Muestra la prueba de red:** Abre la pestaña "Network" (Red) de las herramientas de desarrollador del navegador (F12) y recarga la página. Muestra que la petición a `/api/productos` responde 200 OK.
*   **Di:** *"Aquí demostramos que el frontend está proxyando la solicitud al backend por la red privada interna de Docker Compose (`app-network`). El backend Node.js a su vez está conectado a la Base de Datos MySQL."*

## Minuto 3:00 - 4:00 | 4. Evidencia de Docker desde la Terminal
*   **Abre tu terminal SSH o Session Manager de AWS a la instancia EC2.**
*   Ejecuta: `docker ps`
*   **Di:** *"Aquí están los 3 contenedores corriendo. Note los nombres explícitos y el enrutamiento de puertos."*
*   Ejecuta: `docker images`
*   **Di:** *"Estas son las imágenes optimizadas construidas vía Multi-stage. El uso de Alpine redujo drásticamente su peso."*

## Minuto 4:00 - 5:00 | 5. Demostración de Persistencia
*   En la misma terminal, ejecuta: `docker volume ls`
*   **Di:** *"Vemos aquí el Named Volume `tienda_db_data`. Gracias a esto, si eliminamos el contenedor de base de datos..."*
*   *(Acción opcional si quieres impresionar:)* `docker rm -f tienda-db` y luego `docker-compose up -d`
*   **Di:** *"...Al volver a levantar el contenedor, no perdemos el inventario de la tienda porque los datos residen seguros en el host administrado por Docker."*

*Cierra agradeciendo la atención.*
