# ==========================================
# Etapa 1: Build (Dummy en este caso, solo para cumplir multi-stage)
# Si hubiera React/Angular aquí iría el npm run build
# ==========================================
FROM alpine AS builder
WORKDIR /app
COPY index.html app.js ./

# ==========================================
# Etapa 2: Producción con Nginx unprivileged
# ==========================================
FROM nginxinc/nginx-unprivileged:alpine

# Copiar archivos estáticos de la etapa anterior
COPY --from=builder /app/index.html /usr/share/nginx/html/
COPY --from=builder /app/app.js /usr/share/nginx/html/

# Copiar template de configuración para que envsubst actúe al iniciar
COPY templates/default.conf.template /etc/nginx/templates/default.conf.template

# Exponer puerto para el usuario no root
EXPOSE 8080

# Healthcheck para evaluar la disponibilidad de Nginx
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/ || exit 1

# Variables de entorno por defecto
ENV BACKEND_HOST=backend
ENV BACKEND_PORT=3001