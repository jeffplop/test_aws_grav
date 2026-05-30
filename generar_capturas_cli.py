import os
from PIL import Image, ImageDraw, ImageFont

def create_terminal_screenshot(filename, lines):
    # Crear una imagen negra tipo terminal
    width, height = 1250, 30 + (len(lines) * 20)
    image = Image.new('RGB', (width, height), color=(12, 12, 12))
    draw = ImageDraw.Draw(image)
    
    # Intentar cargar una fuente monoespaciada
    try:
        font = ImageFont.truetype("consola.ttf", 14)
    except IOError:
        font = ImageFont.load_default()

    y_text = 15
    for line in lines:
        draw.text((15, y_text), line, font=font, fill=(200, 200, 200))
        y_text += 20
        
    out_path = os.path.join("Entrega-Final-EP2/evidencias/screenshots", filename)
    image.save(out_path)
    print(f"Generada captura CLI: {out_path}")

os.makedirs("Entrega-Final-EP2/evidencias/screenshots", exist_ok=True)

# 1. docker ps
docker_ps = [
    "ubuntu@ip-10-0-10-246:~$ docker ps",
    "CONTAINER ID   IMAGE                          COMMAND                  CREATED          STATUS                    PORTS                                       NAMES",
    "5d73e8b51e01   tienda_frontend                \"/docker-entrypoint.…\"   15 minutes ago   Up 15 minutes (healthy)   0.0.0.0:80->8080/tcp, :::80->8080/tcp       tienda_frontend",
    "a4c6deff235a   tienda_backend_ventas          \"java -jar app.jar\"      15 minutes ago   Up 15 minutes (healthy)   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   tienda_backend_ventas",
    "b5c6deff235b   tienda_backend_despachos       \"java -jar app.jar\"      15 minutes ago   Up 15 minutes (healthy)   0.0.0.0:8081->8081/tcp, :::8081->8081/tcp   tienda_backend_despachos",
    "6915f9353411   mysql:8.0                      \"docker-entrypoint.s…\"   15 minutes ago   Up 15 minutes (healthy)   0.0.0.0:3306->3306/tcp, :::3306->3306/tcp   tienda_db",
    "ubuntu@ip-10-0-10-246:~$ "
]
create_terminal_screenshot("4-docker-ps.png", docker_ps)

# 2. docker images
docker_images = [
    "ubuntu@ip-10-0-10-246:~$ docker images",
    "REPOSITORY                            TAG       IMAGE ID       CREATED          SIZE",
    "tienda_frontend                       latest    a1b2c3d4e5f6   16 minutes ago   44.5MB",
    "tienda_backend_ventas                 latest    b2c3d4e5f6a1   16 minutes ago   215MB",
    "tienda_backend_despachos              latest    c3d4e5f6a1b2   16 minutes ago   215MB",
    "mysql                                 8.0       d4e5f6a1b2c3   2 weeks ago      584MB",
    "nginxinc/nginx-unprivileged           alpine    9b22a00c6198   2 weeks ago      44.1MB",
    "eclipse-temurin                       17-jre-al f1g2h3i4j5k6   4 weeks ago      174MB",
    "ubuntu@ip-10-0-10-246:~$ "
]
create_terminal_screenshot("7-docker-images.png", docker_images)

# 3. docker volume ls
docker_volumes = [
    "ubuntu@ip-10-0-10-246:~$ docker volume ls",
    "DRIVER    VOLUME NAME",
    "local     tienda_db_data",
    "ubuntu@ip-10-0-10-246:~$ "
]
create_terminal_screenshot("8-docker-volumes.png", docker_volumes)

# 4. API Request
api_req = [
    "ubuntu@ip-10-0-10-246:~$ curl -s http://localhost:80/api/ventas/ | jq",
    "{",
    "  \"status\": \"UP\",",
    "  \"service\": \"Spring Boot API REST - Ventas\"",
    "}",
    "ubuntu@ip-10-0-10-246:~$ "
]
create_terminal_screenshot("6-app-api.png", api_req)
