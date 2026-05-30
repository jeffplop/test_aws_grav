# 🧠 Guía de Estudio a Prueba de Fallos (Defensa del Proyecto)

Tranquilo, no necesitas ser un experto programador para sacar un 7.0. Solo necesitas entender **para qué sirve cada cosa** usando palabras simples. Lee esto un par de veces y estarás más que preparado.

---

## 🏗️ 1. Nuestra Arquitectura (El Restaurante)
En lugar de tener un programa gigante donde todo está mezclado (un Monolito), nosotros separamos el proyecto en **4 partes independientes (Microservicios)**. Imagina que el sistema es un restaurante:

1. **Frontend (React Vite)**: Es el *Mesero*. Es la pantalla verde que ve el usuario. Pide datos y los muestra, pero no procesa nada complejo.
2. **Backend Ventas (Java Spring Boot)**: Es el *Cajero*. Solo se encarga del dinero y de saber qué compraron.
3. **Backend Despachos (Java Spring Boot)**: Es el *Repartidor*. Solo se encarga de saber si la caja ya fue enviada o no.
4. **Base de Datos (MySQL)**: Es la *Bodega*. Donde se guarda la información (las tablas) para que no se pierda.

**Ventaja principal:** Si el "cajero" (ventas) se enferma y se cae, el "repartidor" (despachos) sigue funcionando. Esa es la magia de los microservicios.

---

## 🐳 2. Docker y Docker Compose (Las Cajas de Mudanza)
*   **Docker:** Es una herramienta para meter cada uno de nuestros 4 programas en "cajas blindadas" (Contenedores). Al meter el Frontend en una caja, garantizamos que funcionará igual en tu PC, en la del profe y en la nube de Amazon. Nadie puede decir *"en mi compu sí funcionaba"*.
*   **Docker Compose:** Es como el *jefe de la mudanza*. Es un archivo (`docker-compose.yml`) que le dice a Docker: *"Levanta las 4 cajas juntas, conéctalas con un cable de red invisible (app-network) y asegúrate de encender la Base de Datos primero"*.

---

## 🤖 3. CI/CD con GitHub Actions (La Fábrica de Robots)
CI/CD significa *Integración Continua y Despliegue Continuo*. 
*   **Antes:** Para actualizar la página, tenías que entrar manualmente al servidor, copiar los archivos, apagar todo y volver a encenderlo.
*   **Lo que hicimos:** Configuramos unos "robots" en GitHub (los archivos YAML). Ahora, cuando tú modificas código y haces un `git push`, el robot se despierta, compila el código, lo empaqueta y lo instala en Amazon Web Services de forma **100% automática**.

---

## ☁️ 4. Amazon Web Services (AWS)
Usamos dos servicios clave de AWS:
1.  **ECR (Elastic Container Registry):** Es como un *Estacionamiento Privado*. GitHub envía las imágenes (contenedores) ahí para guardarlas seguras en la nube.
2.  **EC2 (Elastic Compute Cloud):** Es una *Computadora alquilada por internet*. Ahí es donde finalmente se ejecuta nuestro proyecto (la IP pública que pones en el navegador).

---

## 🚨 Preguntas Trampa del Profesor (Y cómo responderlas)

**Pregunta 1: *"¿Por qué dicen que su contenedor es más seguro?"***
> **Tu respuesta:** "Porque usamos *Multi-stage builds* y un usuario *Non-root*. Esto significa que borramos toda la basura de compilación y dejamos una imagen diminuta de Alpine Linux. Además, nuestro servidor Java corre con el usuario 'spring' y nuestro Frontend con 'nginx-unprivileged'. Si un hacker entra, no tendrá permisos de Administrador para borrar nada."

**Pregunta 2: *"¿Qué pasa con los datos de MySQL si se destruye el contenedor de la Base de Datos?"***
> **Tu respuesta:** "No pasa nada, profesor. Configuramos un *Volumen de Docker* (llamado tienda_db_data). El volumen actúa como un disco duro externo. Si el contenedor explota, cuando nazca uno nuevo, se conectará al volumen y recuperará toda la información intacta."

**Pregunta 3: *"Si tengo el Frontend y el Backend en diferentes contenedores, ¿Cómo se comunican sin abrir puertos inseguros?"***
> **Tu respuesta:** "Están todos dentro de la misma red privada de Docker llamada 'app-network'. Solo abrimos el puerto 80 del Frontend hacia el internet. El Frontend (usando Nginx como Proxy Reverso) se encarga de reenviar las peticiones hacia los Backends de manera interna y segura. El mundo exterior ni siquiera sabe que los backends existen."
