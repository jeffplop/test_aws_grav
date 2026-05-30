# 🍺 Traductor de las "Preguntas del Amigo" (Defensa Avanzada)

Lo que te dijo tu amigo tomando cervezas es **oro puro**. Son exactamente las cosas en las que los profesores se fijan para pillar a los alumnos que no hicieron el trabajo. 

Aquí te traduzco lo que quiso decir y te doy la respuesta exacta que debes dar si el profe te ataca por ahí.

---

### 1. "Sssh Instancias - docket fly - docket compose lo que es"
**Lo que quiso decir:** Te van a preguntar si te conectaste a tu instancia por SSH (consola negra) y la diferencia entre Dockerfile y Docker Compose.
**Tu respuesta experta:** 
> "Profesor, nosotros tomamos la decisión arquitectónica de **NO usar SSH** (Puerto 22) para el despliegue automático. En su lugar, usamos **AWS SSM (Systems Manager)** desde GitHub Actions, lo cual es mil veces más seguro porque evita exponer el servidor a ataques de fuerza bruta en internet. 
> Sobre Docker: El `Dockerfile` es simplemente la receta para crear la imagen de un solo programa (ej. React). Pero usamos `docker-compose` porque es el orquestador: levanta los 4 contenedores al mismo tiempo y los conecta en una red privada."

---

### 2. "Base de datos lo que se implementó su instancia subido al compose"
**Lo que quiso decir:** Te preguntarán por qué la Base de Datos está en el `docker-compose` y no instalada directamente en el servidor.
**Tu respuesta experta:**
> "Nuestra base de datos MySQL 8 corre como un contenedor dentro del `docker-compose`. La gran ventaja de esto es que es **100% portable**. Si se quema el servidor de Amazon hoy, mañana corremos el mismo compose en otra computadora y la base de datos se levanta sola con las mismas contraseñas. Y para no perder los datos, le configuramos un **Named Volume** (Volumen de Docker) que guarda la información físicamente en el disco duro del servidor."

---

### 3. "Application properties base de datos pa las líneas..."
**Lo que quiso decir:** El profe revisa el archivo `application.properties` de Java. Si tienes escrito `localhost:3306` directamente ahí, repruebas porque en la nube no funciona así.
**Tu respuesta experta:**
> "Si revisa nuestro código en Java (`application.properties`), verá que NO escribimos la IP directamente. Usamos **Variables de Entorno** (ejemplo: `${DB_ENDPOINT}`). Así, cuando GitHub instala el proyecto, el `docker-compose` le inyecta dinámicamente el nombre del contenedor de la base de datos. Esto es un estándar de la industria (12-Factor App) para no quemar credenciales en el código."

---

### 4. "Prioridad aws deploy automático explicar sr yml que es..."
**Lo que quiso decir:** Tienes que explicar paso a paso qué es el archivo `.yml` y qué pasa cuando haces `git push`.
**Tu respuesta experta:**
> "El archivo `.yml` es el 'cerebro' de nuestra automatización (CI/CD). Cuando hacemos un `git push` a la rama `deploy`, ocurre lo siguiente en cadena:
> 1. GitHub lee el YAML e inicia una máquina virtual temporal.
> 2. Se loguea en nuestra cuenta de Amazon usando los *Secrets*.
> 3. Construye la imagen Docker y la sube al repositorio **Amazon ECR**.
> 4. Finalmente, le manda un ping a nuestra instancia EC2 para decirle: *'Oye, hay una versión nueva, descárgala con docker-compose y reinicia'*. Todo sin intervención humana."

---

### 5. "La IP cambia en la wea de cerrar aws p demás IP estática"
**Lo que quiso decir:** Cuando apagas AWS Academy (End Lab), Amazon te quita la IP pública. Al día siguiente te da una IP totalmente distinta y pierdes el acceso a tu página web si la tenías guardada.
**Tu respuesta experta:**
> "Es correcto, al ser una cuenta de laboratorio de AWS Academy, la IP pública es efímera y cambia cada vez que apagamos el laboratorio. La solución empresarial real sería asignarle una **Elastic IP (IP Estática)** desde la consola de AWS, lo que la dejaría fija para siempre. Sin embargo, para fines de esta evaluación, simplemente obtenemos la nueva IP generada por EC2 cada vez que iniciamos el laboratorio."

---

### 6. "Mostrar comandos ppt de que funciona..."
**Lo que quiso decir:** El profe quiere ver capturas de pantalla de la consola demostrando que tú escribiste comandos de Docker.
**Tu respuesta experta:**
> (Solo tienes que mostrar las imágenes que yo incrusté en el PowerPoint y en el HTML).
> "Como se aprecia en la captura, al ejecutar `docker ps` se ven los 4 contenedores activos (`tienda_frontend`, `tienda_backend_ventas`, `tienda_backend_despachos` y `tienda_db`). Y con `docker volume ls` demostramos que el disco duro de la base de datos está montado correctamente."
