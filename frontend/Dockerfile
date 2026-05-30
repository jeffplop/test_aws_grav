# Etapa 1: Construcción (Builder)
FROM node:18-alpine AS builder
WORKDIR /app

# Copiar archivos de dependencias
COPY package.json package-lock.json ./
RUN npm install

# Copiar el código fuente
COPY . .

# Compilar la aplicación React con Vite
RUN npm run build

# Etapa 2: Producción (Servidor Nginx Non-root)
FROM nginxinc/nginx-unprivileged:alpine

# Copiar los assets compilados desde la etapa anterior
COPY --from=builder /app/dist /usr/share/nginx/html

# Crear directorios para los templates
USER root
RUN mkdir -p /etc/nginx/templates
USER nginx

# Copiar la plantilla de configuración (Proxy Reverso dinámico)
COPY templates/default.conf.template /etc/nginx/templates/default.conf.template

# Exponer el puerto 8080 (el usuario es non-root)
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
