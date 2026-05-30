# ==========================================
# Etapa 1: Build y dependencias
# ==========================================
FROM node:18-alpine AS builder

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de definición de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm install --production

# ==========================================
# Etapa 2: Producción
# ==========================================
FROM node:18-alpine

# Instalar curl para el HEALTHCHECK (opcional pero recomendado)
RUN apk --no-cache add curl

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar dependencias de la etapa builder
COPY --from=builder /app/node_modules ./node_modules

# Copiar el código fuente de la aplicación
COPY . .

# Cambiar la propiedad de los archivos al usuario no root 'node' (incluido en la imagen node)
RUN chown -R node:node /app

# Cambiar a usuario no root por seguridad
USER node

# Exponer el puerto
EXPOSE 3001

# Configurar HEALTHCHECK para asegurar que el contenedor está funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3001/api/health || exit 1

# Comando por defecto
CMD ["npm", "start"]
