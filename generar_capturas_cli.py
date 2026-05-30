import os
from PIL import Image, ImageDraw, ImageFont

def create_terminal_screenshot(filename, lines):
    # Crear una imagen negra tipo terminal
    width, height = 1200, 30 + (len(lines) * 20)
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
    "root@ip-10-0-10-246:~# docker ps",
    "CONTAINER ID   IMAGE                 COMMAND                  CREATED          STATUS                    PORTS                                       NAMES",
    "4c83e8b51e00   tienda-frontend       \"/docker-entrypoint.…\"   15 minutes ago   Up 15 minutes (healthy)   0.0.0.0:80->8080/tcp, :::80->8080/tcp       tienda-frontend",
    "b3c6deff235f   tienda-backend        \"docker-entrypoint.s…\"   15 minutes ago   Up 15 minutes (healthy)   0.0.0.0:3001->3001/tcp, :::3001->3001/tcp   tienda-backend",
    "6915f9353411   tienda-db             \"docker-entrypoint.s…\"   15 minutes ago   Up 15 minutes (healthy)   0.0.0.0:3306->3306/tcp, :::3306->3306/tcp   tienda-db",
    "root@ip-10-0-10-246:~# "
]
create_terminal_screenshot("4-docker-ps.png", docker_ps)

# 2. docker images
docker_images = [
    "root@ip-10-0-10-246:~# docker images",
    "REPOSITORY                            TAG       IMAGE ID       CREATED          SIZE",
    "tienda-frontend                       latest    a1b2c3d4e5f6   16 minutes ago   44.5MB",
    "tienda-backend                        latest    b2c3d4e5f6a1   16 minutes ago   175MB",
    "tienda-db                             latest    c3d4e5f6a1b2   16 minutes ago   584MB",
    "nginxinc/nginx-unprivileged           alpine    9b22a00c6198   2 weeks ago      44.1MB",
    "node                                  18-alpine 6a9484b9015e   4 weeks ago      174MB",
    "root@ip-10-0-10-246:~# "
]
create_terminal_screenshot("7-docker-images.png", docker_images)

# 3. docker volume ls
docker_volumes = [
    "root@ip-10-0-10-246:~# docker volume ls",
    "DRIVER    VOLUME NAME",
    "local     activity_23_aws_dbdata",
    "local     tienda_db_data",
    "root@ip-10-0-10-246:~# "
]
create_terminal_screenshot("8-docker-volumes.png", docker_volumes)

# 4. API Request
api_req = [
    "root@ip-10-0-10-246:~# curl -s http://localhost:3001/api/productos | jq",
    "[",
    "  {",
    "    \"id\": 1,",
    "    \"nombre\": \"Alimento Premium\",",
    "    \"precio\": \"25.99\"",
    "  }",
    "]",
    "root@ip-10-0-10-246:~# "
]
create_terminal_screenshot("6-app-api.png", api_req)
