import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

local_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Roaming', 'Python', 'Python313', 'site-packages')
if local_path not in sys.path:
    sys.path.append(local_path)

def add_slide(prs, title, text_content=None, image_path=None):
    layout = prs.slide_layouts[1] if text_content else prs.slide_layouts[5]
    slide = prs.slides.add_slide(layout)
    
    title_shape = slide.shapes.title
    title_shape.text = title
    for paragraph in title_shape.text_frame.paragraphs:
        paragraph.font.name = 'Arial'
        paragraph.font.size = Pt(36)
        paragraph.font.bold = True
        paragraph.font.color.rgb = RGBColor(35, 47, 62)
        
    if text_content:
        body = slide.placeholders[1]
        tf = body.text_frame
        tf.clear()
        for line in text_content.split('\n'):
            p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(20)
            p.font.name = 'Arial'
            p.space_after = Pt(14)
            p.font.color.rgb = RGBColor(60, 60, 60)

    if image_path and os.path.exists(image_path):
        left = Inches(4.5) if text_content else Inches(1)
        top = Inches(2.5) if text_content else Inches(1.8)
        height = Inches(4)
        try:
            slide.shapes.add_picture(image_path, left, top, height=height)
        except Exception as e:
            pass

def create_modern_pptx():
    prs = Presentation()
    
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "Innovatech Chile: Proyecto Semestral DevOps"
    subtitle.text = "Evaluación Parcial 2 - Defensa Técnica\nArquitectura Java Spring Boot & React Vite en AWS"
    
    for paragraph in title.text_frame.paragraphs:
        paragraph.font.bold = True
        paragraph.font.color.rgb = RGBColor(255, 153, 0)

    add_slide(prs, "Contexto: Proyecto Semestral", 
              "Objetivo: Desplegar plataforma de microservicios en AWS.\n"
              "Arquitectura:\n"
              "1. Frontend React (Vite).\n"
              "2. Backend Ventas (Java Spring Boot).\n"
              "3. Backend Despachos (Java Spring Boot).\n"
              "4. Database MySQL compartida.\n"
              "Automatización total vía GitHub Actions a Amazon EC2.")

    add_slide(prs, "[IE1/IE6] Diseño de Contenedorización", 
              "Backends (Java Maven):\n"
              "• Multi-stage: 'maven' compila, 'temurin-jre-alpine' corre.\n"
              "• Seguridad: Ejecutados con usuario 'spring' (non-root).\n\n"
              "Frontend (React Vite):\n"
              "• Multi-stage: 'node' compila, Nginx sirve estáticos.\n"
              "• Seguridad: nginxinc/nginx-unprivileged (Puerto 8080).\n"
              "• Enrutamiento: Nginx actúa como Proxy Reverso (/api/*).")

    add_slide(prs, "[IE2/IE6] Docker Compose y Persistencia", 
              "Orquestación (4 Servicios):\n"
              "• Red Interna: 'app-network' aísla microservicios.\n"
              "Persistencia de Datos:\n"
              "• Elección: Named Volume ('tienda_db_data').\n"
              "• Justificación: Named Volumes aíslan datos del host Linux,\n"
              "  mejorando la portabilidad y seguridad vs Bind Mounts.\n"
              "• Alta Disponibilidad: Datos sobreviven a redespliegues.")

    add_slide(prs, "[IE3] Pipeline CI/CD: 3 Flujos", 
              "Pipelines Independientes por Microservicio:\n"
              "• cicd-tienda-frontend.yml\n"
              "• cicd-tienda-backend-ventas.yml\n"
              "• cicd-tienda-backend-despachos.yml\n"
              "Flujo (Push a rama 'deploy'):\n"
              "1. Build & Push imagen a Amazon ECR.\n"
              "2. Trigger SSM para EC2: Docker Compose Pull & Up.",
              "Entrega-Final-EP2/evidencias/diagramas/2-flujo-cicd.png")

    add_slide(prs, "[IE7] Justificación Técnica del Despliegue", 
              "¿Por qué Amazon ECR?\n"
              "• Integración nativa con IAM y latencia cero hacia EC2.\n"
              "¿Por qué AWS Systems Manager (SSM)?\n"
              "• Permite comandos remotos automatizados en EC2.\n"
              "• Innovatech Chile no necesita abrir puertos SSH al mundo,\n"
              "  mitigando vulnerabilidades críticas en producción.",
              "Entrega-Final-EP2/evidencias/screenshots/3-github-actions.png")

    add_slide(prs, "[IE8] Principios DevOps Aplicados", 
              "1. Microservicios: Desacoplamiento Ventas/Despachos.\n"
              "2. Shift-Left Security: Alpine Linux y usuarios Non-Root.\n"
              "3. Entrega Continua: Lead Time minimizado con GH Actions.\n"
              "4. IaC: Todo orquestado nativamente con Compose.\n"
              "Escalabilidad: La arquitectura Spring Boot + React está\n"
              "lista para la Nube.")

    add_slide(prs, "[IE4/IE9] Funcionamiento de Microservicios", 
              "El Nginx (Frontend) es el único expuesto al público.\n"
              "Ambos backends Spring Boot (8080 y 8081) y MySQL (3306)\n"
              "están ocultos en la subred privada de Docker.\n"
              "El Proxy de Nginx resuelve peticiones /api/ internamente.",
              "Entrega-Final-EP2/evidencias/screenshots/5-app-frontend.png")

    add_slide(prs, "Evidencia Técnica: Contenedores Vivos", 
              "Verificación mediante 'docker ps' y 'docker images'.\n"
              "Se aprecian 4 contenedores en ejecución paralela.",
              "Entrega-Final-EP2/evidencias/screenshots/4-docker-ps.png")
              
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "Demostración Funcional en Vivo (IE9)"
    body = slide.placeholders[1]
    tf = body.text_frame
    tf.text = "1. Navegación en Frontend React.\n2. Verificación de logs en Backends Java.\n3. Recuperación de base de datos MySQL (Named Volume).\n4. Despliegue CI/CD automático tras Git Push."

    out_path = "Entrega-Final-EP2/Presentacion-Semestral-EP2.pptx"
    prs.save(out_path)
    print(f"Generado exitosamente: {out_path}")

if __name__ == "__main__":
    create_modern_pptx()
