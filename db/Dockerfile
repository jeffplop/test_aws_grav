# Imagen base MySQL 8 oficial
FROM mysql:8

# Variables de entorno por defecto (idealmente sobreescritas por docker-compose)
ENV MYSQL_ROOT_PASSWORD=admin123
ENV MYSQL_DATABASE=tienda_perritos
ENV MYSQL_USER=alumno
ENV MYSQL_PASSWORD=alumno123

# Copiar el script de inicialización dentro de la imagen
# Se ejecuta automáticamente la primera vez que se levante el contenedor
COPY init.sql /docker-entrypoint-initdb.d/

# Exponer el puerto de MySQL
EXPOSE 3306

# Healthcheck usando mysqladmin ping
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=5 \
  CMD mysqladmin ping -h localhost -uroot -p$MYSQL_ROOT_PASSWORD || exit 1
