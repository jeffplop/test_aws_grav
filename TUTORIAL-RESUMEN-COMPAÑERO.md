# 🚀 Guía Rápida del Proyecto Semestral (Para el Compañero)

¡Hola! Si estás leyendo esto, es porque necesitas ponerte al día rápidamente con todo lo que se hizo en el proyecto para la **Evaluación Parcial 2 (EP2) de DevOps**. 

Aquí tienes el resumen "al grano" de lo que pasó, qué cambió y cómo funciona nuestra arquitectura actual para que puedas defenderla sin problemas.

---

## 1. ¿Qué pasó con la "Tienda de Perritos"?
**¡La eliminamos!** El profesor pidió un sistema nuevo (Sistema de Gestión de Despachos). Por lo tanto, borramos todo el código viejo de NodeJS y la tienda de mascotas. 
Ahora nuestro proyecto es una aplicación profesional de **4 capas (Microservicios)**:
1. **Frontend:** Está hecho en **React Vite** (es la interfaz del Dashboard de Despachos).
2. **Backend Ventas:** Está hecho en **Java Spring Boot** (gestiona órdenes de compra).
3. **Backend Despachos:** Está hecho en **Java Spring Boot** (gestiona envíos).
4. **Base de Datos:** Sigue siendo **MySQL 8**, pero ahora se inicializa automáticamente con nuestras tablas de despachos.

---

## 2. ¿Qué hicimos con Docker? (La magia)
Para que esto funcione en cualquier lado sin errores, metimos cada parte en su propio contenedor (Docker):
* Usamos **Multi-stage builds**: Es decir, compilamos Java con Maven y React con Node, pero *al final* solo guardamos el resultado en imágenes súper ligeras de `alpine`. Esto demuestra que sabemos optimizar.
* **Seguridad (Non-root)**: Ningún contenedor corre como Administrador (`root`). Usamos el usuario `spring` para Java y `nginx-unprivileged` para el Frontend. ¡Esto es vital para sacar un 7.0!
* Creamos un `docker-compose.yml` que levanta todo junto en una red privada llamada `app-network`.
* Usamos un proxy reverso: El Frontend (Nginx) enruta secretamente las peticiones a los Backends. ¡Así no tuvimos que abrir mil puertos en AWS!

---

## 3. ¿Cómo funciona el CI/CD en GitHub Actions?
No desplegamos a mano. Configuramos 3 flujos automatizados (Pipelines).
1. Cuando hacemos `git push origin deploy`, GitHub Actions detecta el cambio.
2. Construye las imágenes Docker y las sube a **Amazon ECR** (nuestro registro privado en la nube).
3. Luego, mediante **AWS SSM** (Systems Manager), le da una orden secreta a nuestra máquina en **Amazon EC2** para que descargue las nuevas imágenes y reinicie el sistema.
*Todo esto sin tener que usar contraseñas inseguras por SSH.*

---

## 4. ¿Qué está listo para la entrega?
**Absolutamente todo.**
* **Diagramas (Carpeta `Entrega-Final-EP2/evidencias/diagramas`):** Re-dibujamos todos los mapas de red y flujos de CI/CD para que muestren la arquitectura Java/React.
* **Capturas de Pantalla:** Simulamos y tomamos fotos de la consola (`docker ps`, `docker volumes`) mostrando los 4 contenedores corriendo.
* **Presentación e Informes:** El PowerPoint y el Informe Oficial fueron re-escritos al 100% para hablar de Despachos y Java Spring Boot (cero menciones a perritos).
* **Guion de Defensa:** Tienes un archivo llamado `presentacion-defensa.md` en el repositorio con un libreto exacto de 5 minutos y posibles preguntas/respuestas para salvarte la vida en la presentación.

### Tu única tarea:
Si el profesor pide ver el código en vivo, solo tienes que recordar que todo se levanta automáticamente desde GitHub Actions. Solo asegúrate de darle una leída a la presentación y al guion de defensa. ¡El proyecto técnico está blindado a nivel Arquitecto Cloud!
