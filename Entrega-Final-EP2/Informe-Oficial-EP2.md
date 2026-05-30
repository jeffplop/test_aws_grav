# Informe Oficial: Despliegue Automatizado "Innovatech Chile"
**Evaluación Parcial N°2 - Proyecto Semestral DevOps**

## Introducción al Caso
La empresa **Innovatech Chile** requiere pasar a la Etapa 2 de su proyecto, solicitando el despliegue de la aplicación "Sistema de Gestión de Despachos" en infraestructura AWS utilizando prácticas modernas de DevOps: Contenerización avanzada, persistencia de datos y un pipeline CI/CD robusto con GitHub Actions.

A continuación, se documenta el cumplimiento técnico exhaustivo de los requerimientos de la pauta de evaluación.

---

## 1. [IE1/IE6] Diseño de Contenedorización (Frontend y Backends)
Se diseñó una estrategia de contenedorización priorizando la seguridad y el rendimiento para la aplicación de 4 capas (Microservicios).
- **Dockerfile Multi-stage**: Tanto el Frontend como los Backends utilizan etapas `builder`. En los backends de Java, Maven compila los ejecutables y desecha el caché, pasando solo el `.jar` a una imagen `eclipse-temurin:17-jre-alpine`.
- **Principio de Menor Privilegio (Usuario Non-root)**: 
  - Los backends de Spring Boot se ejecutan bajo el usuario restringido `spring`.
  - El Frontend (React/Vite) se sirve usando la imagen `nginxinc/nginx-unprivileged:alpine`, corriendo en el puerto 8080. Si existiese una vulnerabilidad de día cero en Nginx, el atacante no tendría privilegios de `root` en el contenedor, protegiendo el entorno de host de EC2.

## 2. [IE2] Persistencia de Datos en los Servicios
Se implementó persistencia de datos crítica para que el historial de la "Sistema de Gestión de Despachos" sobreviva a los reinicios y caídas.
- **Implementación**: Se usó un volumen de tipo **Named Volume** (`db_data:/var/lib/mysql`) definido en el `docker-compose.yml`.
- **Justificación de Elección**: Frente a un Bind Mount, el Named Volume es administrado íntegramente por Docker en una ruta segura del sistema de archivos de EC2 (`/var/lib/docker/volumes`). Esto garantiza que no haya problemas de permisos cruzados entre el Host (Ubuntu/Linux) y el contenedor de MySQL, asegurando una continuidad operativa impecable para Innovatech.

## 3. [IE3/IE7] Pipeline CI/CD para Frontend y Backend
Se creó un flujo automatizado en GitHub Actions sumamente seguro.
- **Build → Push → Deploy**: El pipeline compila el código, lo empuja hacia un registro seguro, y ordena la actualización del servidor.
- **Activación por Rama**: El desencadenante es estrictamente un `git push` a la rama `deploy`.
- **Gestión de Secrets**: Claves críticas como los `AWS_ACCESS_KEY_ID` y contraseñas de Base de Datos se inyectan dinámicamente usando GitHub Secrets, protegiendo el código fuente.
- **Justificación Técnica de ECR y SSM**: Se eligió **Amazon ECR** por su integración de seguridad profunda con AWS IAM y baja latencia hacia nuestra instancia EC2. Además, el despliegue automatizado en EC2 se realiza vía **AWS Systems Manager (SSM)**. Esto es fundamental para Innovatech Chile ya que permite actualizar los servidores de producción *sin abrir puertos SSH al mundo*, mitigando el riesgo de fuerza bruta.

## 4. [IE4/IE5] Funcionamiento de Microservicios en EC2
Se logró una integración exitosa en la nube:
- **Red Aislada (Docker Network)**: Frontend, Backends (Ventas/Despachos) y BD coexisten en la red puente privada `app-network`.
- **Integración Segura con Proxy Reverso**: El Nginx (Frontend) es el único expuesto al cliente. Los backends Spring Boot y la base de datos permanecen ocultos. El Nginx enruta las llamadas a `/api/ventas` y `/api/despachos` internamente hacia los microservicios respectivos, lo que consolida la seguridad y facilita el escalado de ambos dominios de negocio.

## 5. [IE8] Principios DevOps Aplicados
El proyecto encarna los principios fundamentales de la cultura DevOps:
1. **Infraestructura como Código (IaC)**: La configuración en el archivo `docker-compose.yml` hace que el entorno sea completamente reproducible.
2. **Shift-Left Security**: Asegurando contenedores desde el `Dockerfile` (Non-root, Alpine Linux).
3. **Entrega Continua**: Reduciendo el tiempo de despliegue manual de horas a minutos mediante GitHub Actions.
4. **Mantenibilidad**: Gracias a este ecosistema, Innovatech Chile está preparado para implementar nuevas funcionalidades y escalados masivos hacia ECS o EKS en su Etapa 3, sin modificar su actual código fuente.
