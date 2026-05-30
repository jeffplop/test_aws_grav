# Etapa 1: Compilación (Maven Builder)
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app

# Copiar el pom.xml y descargar dependencias (para cachear)
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copiar el código fuente y compilar
COPY src ./src
RUN mvn clean package -DskipTests

# Etapa 2: Producción (JRE 17 Ligero y Seguro)
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# Crear un grupo y usuario sin privilegios
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

# Copiar el ejecutable .jar generado en la etapa anterior
COPY --from=builder /app/target/*.jar app.jar

# Exponer el puerto configurado en application.properties (8080 default o configurado)
EXPOSE 8080

# Comando para ejecutar la aplicación
ENTRYPOINT ["java", "-jar", "app.jar"]
