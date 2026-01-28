# MCP Server Architecture

## 📁 Project Structure

```
mcp_server/
├── mcp_server.py          # Main server entry point
├── config/
│   └── settings.py        # Configuration management
├── core/
│   └── factory.py         # MCP server factory and base classes
├── services/              # Business logic modules
│   ├── bb_demo_service.py
│   ├── demo_general_service.py
│   └── demo_tech_support_service.py
└── utils/
    ├── tracing.py         # OpenTelemetry utilities
    ├── date_utils.py      # Date/time helpers
    └── formatters.py      # Response formatters
```

## 🏗️ Core Components

### 1. Main Server (`mcp_server.py`)
- **Purpose**: Application entry point and server initialization
- **Responsibilities**:
  - Create MCPToolFactory instance
  - Register all services
  - Configure authentication (optional)
  - Add health check endpoint
  - Start server

### 2. Services (`services/`)
- **Purpose**: Modular business logic organization
- **Pattern**: Each service implements `MCPToolBase`
- **Structure**:
  ```python
  class ServiceName(MCPToolBase):
      def __init__(self):
          super().__init__(Domain.NAME)
      
      def register_tools(self, mcp: FastMCP) -> None:
          @mcp.tool(...)
          @trace_tool_call
          def tool_function(...):
              # Implementation
  ```

### 3. Tracing Utilities (`utils/tracing.py`)
- **Purpose**: Centralized OpenTelemetry management
- **Features**:
  - Auto-initialization when `ENABLE_OTEL=true`
  - `@trace_span(name)` - Generic tracing decorator
  - `@trace_tool_call` - MCP tool-specific tracing
- **Design**: Conditionally active, zero overhead when disabled

### 4. Factory Pattern (`core/factory.py`)
- **Purpose**: Service registration and MCP server creation
- **Benefits**:
  - Decoupled service management
  - Easy to add/remove services
  - Centralized tool counting and summaries

## 🔄 Request Flow

```
Client Request
    ↓
FastMCP Server (HTTP/SSE)
    ↓
ASGI Middleware (Auto-instrumentation)
    ↓
MCP Protocol Handler
    ↓
Tool Dispatcher
    ↓
@trace_tool_call decorator
    ↓
Service Tool Function
    ↓
Response → Client
```

## 📊 OpenTelemetry Integration

### Automatic Instrumentation
- **Entrypoint**: `opentelemetry-instrument` wrapper in `entrypoint.sh`
- **Captures**:
  - HTTP requests (ASGI)
  - Outbound HTTP calls (HTTPX)
  - Application lifecycle

### Manual Instrumentation
- **Tool Calls**: `@trace_tool_call` decorator
  - Span name: `mcp.tool.{function_name}`
  - Attributes: tool name, args, result, errors
- **Custom Spans**: `@trace_span(name)` decorator
  - Health checks
  - Custom operations

### Trace Hierarchy
```
HTTP POST /mcp
  └─ mcp.tool.add_two_numbers
      ├─ tool.name: "add"
      ├─ tool.args: "(5, 3)"
      └─ tool.result: "8"
```

## 🎯 Design Principles

### 1. Modularity
- Services are independent and self-contained
- Easy to add new services without modifying core code
- Clear separation of concerns

### 2. Simplicity
- Minimal boilerplate in service definitions
- Decorators handle cross-cutting concerns (tracing)
- Configuration via environment variables

### 3. Observability
- Optional tracing with zero code changes when disabled
- Comprehensive span coverage
- Detailed attributes for debugging

### 4. Flexibility
- Domain-based service organization
- Tag-based tool categorization
- Pluggable authentication

## 🔧 Adding a New Service

1. **Create service class**:
```python
# services/my_service.py
from core.factory import MCPToolBase, Domain
from utils.tracing import trace_tool_call

class MyService(MCPToolBase):
    def __init__(self):
        super().__init__(Domain.MY_DOMAIN)
    
    def register_tools(self, mcp):
        @mcp.tool(tags={self.domain.value})
        @trace_tool_call
        def my_tool(param: str) -> str:
            return f"Processed: {param}"
```

2. **Register in main server**:
```python
# mcp_server.py
from services.my_service import MyService

factory.register_service(MyService())
```

That's it! The tool is automatically:
- Registered with MCP
- Traced in OpenTelemetry
- Counted in summaries

## 🌐 Configuration

### Environment Variables
- `ENABLE_OTEL` - Enable/disable OpenTelemetry (default: false)
- `OTEL_SERVICE_NAME` - Service name in traces
- `OTEL_EXPORTER_OTLP_ENDPOINT` - Collector endpoint
- `MCP_ENABLE_AUTH` - Enable JWT authentication
- `MCP_SERVER_NAME` - Display name for server

### Startup Flow
1. Load environment configuration
2. Initialize OpenTelemetry (if enabled)
3. Create service instances
4. Register tools with MCP
5. Start HTTP server
6. Export traces to collector

## 📈 Observability Stack

```
MCP Server (Port 9000)
    ↓ OTLP/gRPC
OTEL Collector (Port 4317)
    ↓
Jaeger (Port 16686) + Prometheus (Port 9090)
```

View traces: http://localhost:16686
