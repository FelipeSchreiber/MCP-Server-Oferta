# BB MCP4J Server

A Java-based Model Context Protocol (MCP) server using LangChain4j for the Multi-Agent Custom Automation Engine (BB) solution accelerator.

## Overview

This is a Java implementation of the BB MCP Server, mirroring the Python FastMCP implementation but built on Spring Boot and LangChain4j. It provides a RESTful API for MCP tool execution with support for multiple domains, authentication, and containerized deployment.

## Features

- **LangChain4j Integration**: Leverages LangChain4j for AI agent tool definitions
- **Spring Boot Framework**: Built on Spring Boot 3.2 for robust REST API support
- **Factory Pattern**: Reusable MCP tools factory for easy service management
- **Domain-Based Organization**: Services organized by business domains (Demo, Tech Support, General)
- **Authentication**: Optional Azure AD authentication support via OAuth2
- **RESTful API**: HTTP endpoints for tool discovery and execution
- **Docker Support**: Containerized deployment with health checks
- **Maven Build**: Standard Maven project structure
- **Comprehensive Testing**: JUnit 5 test framework

## Architecture

```
mcp4j/
├── src/
│   ├── main/
│   │   ├── java/com/bb/mcp/server/
│   │   │   ├── config/              # Configuration classes
│   │   │   │   └── MCPServerConfig.java
│   │   │   ├── core/                # Core factory and base classes
│   │   │   │   ├── Domain.java
│   │   │   │   ├── MCPToolBase.java
│   │   │   │   └── MCPToolFactory.java
│   │   │   ├── services/            # Domain-specific service implementations
│   │   │   │   ├── BBDemoService.java
│   │   │   │   ├── TechSupportService.java
│   │   │   │   └── GeneralService.java
│   │   │   ├── utils/               # Utility classes
│   │   │   │   ├── DateUtils.java
│   │   │   │   └── ResponseFormatter.java
│   │   │   ├── controller/          # REST API controllers
│   │   │   │   └── MCPController.java
│   │   │   └── MCPServerApplication.java
│   │   └── resources/
│   │       └── application.properties
│   └── test/
│       └── java/com/bb/mcp/server/  # Test classes
├── pom.xml                          # Maven configuration
├── Dockerfile                       # Container configuration
├── docker-compose.yml               # Development container setup
└── README.md                        # This file
```

## Available Services

### BB Demo Service (Domain: demo)
- **add_two_numbers**: Adds two integer numbers together
- **get_user_info**: Retrieves user information by user_id
- **Resources**: Application config, user telephone

### Tech Support Service (Domain: tech_support)
- **reset_password**: Reset password for a user account
- **check_system_status**: Check the operational status of a system

### General Service (Domain: general)
- **get_current_date**: Get the current date in formatted strings
- **format_text**: Format text in various styles (uppercase, lowercase, title)

## Requirements

- Java 17 or higher
- Maven 3.9 or higher
- Docker (optional, for containerized deployment)
- Docker Compose (optional, for containerized deployment)

## Installation

### Local Development

1. **Clone the repository**
   ```bash
   cd "MCP Server Oferta/mcp4j"
   ```

2. **Build the project**
   ```bash
   mvn clean package
   ```

3. **Configure the application**
   
   Edit `src/main/resources/application.properties` or create `.env` file:
   ```properties
   mcp.server.host=0.0.0.0
   mcp.server.port=9000
   mcp.server.enable-auth=false
   ```

4. **Run the application**
   ```bash
   java -jar target/mcp4j-server-1.0.0.jar
   ```
   
   Or using Maven:
   ```bash
   mvn spring-boot:run
   ```

### Docker Deployment

1. **Using Docker Compose (Recommended)**
   ```bash
   docker-compose up -d
   ```

2. **Using Docker directly**
   ```bash
   # Build the image
   docker build -t bb-mcp4j-server .
   
   # Run the container
   docker run -p 9000:9000 \
     -e MCP_SERVER_ENABLE_AUTH=false \
     bb-mcp4j-server
   ```

## API Usage

### Get Server Information
```bash
curl http://localhost:9000/api/mcp/info
```

### List All Tools
```bash
curl http://localhost:9000/api/mcp/tools
```

### Get Tools by Domain
```bash
curl http://localhost:9000/api/mcp/tools/demo
```

### Execute a Tool
```bash
curl -X POST http://localhost:9000/api/mcp/tools/add_two_numbers/execute \
  -H "Content-Type: application/json" \
  -d '{"a": 5, "b": 3}'
```

### Health Check
```bash
curl http://localhost:9000/api/mcp/health
```

## Configuration

### Environment Variables

Configuration can be provided via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_SERVER_HOST` | 0.0.0.0 | Server host address |
| `MCP_SERVER_PORT` | 9000 | Server port |
| `MCP_SERVER_DEBUG` | false | Enable debug mode |
| `MCP_SERVER_SERVER_NAME` | BBMCPServer | Server name |
| `MCP_SERVER_ENABLE_AUTH` | true | Enable authentication |
| `MCP_SERVER_TENANT_ID` | - | Azure AD tenant ID |
| `MCP_SERVER_CLIENT_ID` | - | Azure AD client ID |
| `MCP_SERVER_JWKS_URI` | - | JWKS endpoint URI |
| `MCP_SERVER_ISSUER` | - | Token issuer |
| `MCP_SERVER_AUDIENCE` | - | Token audience |

### application.properties

You can also configure the application using `application.properties`:

```properties
# Server Configuration
mcp.server.host=0.0.0.0
mcp.server.port=9000
mcp.server.debug=false
mcp.server.server-name=BBMCPServer

# Authentication
mcp.server.enable-auth=false
```

## Authentication

The server supports optional Azure AD authentication via OAuth2 JWT tokens.

### Enable Authentication

1. Set `MCP_SERVER_ENABLE_AUTH=true`
2. Configure Azure AD settings:
   ```properties
   mcp.server.tenant-id=your-tenant-id
   mcp.server.client-id=your-client-id
   mcp.server.jwks-uri=https://login.microsoftonline.com/{tenant-id}/discovery/v2.0/keys
   mcp.server.issuer=https://login.microsoftonline.com/{tenant-id}/v2.0
   mcp.server.audience=your-audience
   ```

3. Include JWT token in API requests:
   ```bash
   curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     http://localhost:9000/api/mcp/info
   ```

## Development

### Adding New Services

1. Create a new service class implementing `MCPToolBase`:
   ```java
   @Service
   public class MyNewService implements MCPToolBase {
       private final Domain domain = Domain.MY_DOMAIN;
       
       @Override
       public void registerTools() {
           // Register your tools
       }
       
       @Tool("Description of my tool")
       public String myTool(String param) {
           return "Result";
       }
   }
   ```

2. Add the new domain to `Domain.java` enum if needed

3. Register the service in `MCPServerApplication.java`:
   ```java
   factory.registerService(myNewService);
   ```

### Running Tests

```bash
mvn test
```

### Building

```bash
mvn clean package
```

The built JAR will be in `target/mcp4j-server-1.0.0.jar`

## Troubleshooting

### Port Already in Use
If port 9000 is already in use, change it in the configuration:
```properties
mcp.server.port=9001
```

### Build Failures
Ensure you have Java 17+ and Maven 3.9+:
```bash
java -version
mvn -version
```

### Docker Health Check Fails
Check container logs:
```bash
docker-compose logs mcp4j-server
```

## Dependencies

Key dependencies used in this project:

- **Spring Boot 3.2.1**: Web framework and dependency injection
- **LangChain4j 0.36.2**: AI agent tool framework
- **Azure Identity**: Azure AD authentication
- **Lombok**: Reduce boilerplate code
- **Jackson**: JSON processing
- **JUnit 5**: Testing framework

See [pom.xml](pom.xml) for complete dependency list.

## Comparison with Python Implementation

| Feature | Python (FastMCP) | Java (mcp4j) |
|---------|-----------------|--------------|
| Framework | FastMCP | Spring Boot + LangChain4j |
| Transport | STDIO, HTTP, SSE | REST API |
| Authentication | JWT (FastMCP) | OAuth2 (Spring Security) |
| Tool Definition | @mcp.tool | @Tool + ToolSpecification |
| Configuration | Pydantic | Spring @ConfigurationProperties |
| Build Tool | pip | Maven |
| Container | Python Alpine | OpenJDK Alpine |

## License

Copyright © 2026 Banco do Brasil

## Support

For issues and questions:
- Create an issue in the repository
- Contact the BB Internal Developer Platform team

## Acknowledgments

This project is inspired by and mirrors the Python FastMCP implementation from the Multi-Agent Custom Automation Engine Solution Accelerator.
