# Multi-stage build for BB MCP4J Server with Quarkus
FROM maven:3.9-eclipse-temurin-17-alpine AS builder

# Set working directory
WORKDIR /app

# Copy pom.xml and download dependencies
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application using Quarkus
RUN mvn clean package -DskipTests

# Runtime stage - Use Eclipse Temurin for simplicity
FROM eclipse-temurin:17-jre-alpine

# Set working directory
WORKDIR /app

# Install wget for health check (pin version)
RUN apk add --no-cache wget=1.21.3-r2

# Copy the Quarkus runner from builder stage
COPY --from=builder /app/target/quarkus-app/lib/ /app/lib/
COPY --from=builder /app/target/quarkus-app/*.jar /app/
COPY --from=builder /app/target/quarkus-app/app/ /app/app/
COPY --from=builder /app/target/quarkus-app/quarkus/ /app/quarkus/

# Create a non-root user (Alpine uses addgroup/adduser)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup && chown -R appuser:appgroup /app
USER appuser

# Expose the port
EXPOSE 9000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:9000/api/mcp/health || exit 1

# Run the Quarkus application
ENTRYPOINT ["java", "-jar", "quarkus-run.jar"]

