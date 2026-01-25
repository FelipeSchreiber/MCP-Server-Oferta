# MCP4J Quick Start Guide

## Fixed Issues

✅ **Fixed compilation errors** - Added `<parameters>true</parameters>` to Maven compiler plugin
✅ **Fixed authentication** - Added SecurityConfig to disable auth when `enableAuth=false`
✅ **Fixed docker-compose** - Removed obsolete `version` attribute

## Build and Run

### Using Docker Compose (Recommended)
```bash
cd "MCP Server Oferta/mcp4j"
docker-compose up -d
```

### Check Status
```bash
docker-compose ps
docker logs bb-mcp4j-server
```

### Test the API
```bash
# Health check
curl http://localhost:9000/api/mcp/health

# Server info
curl http://localhost:9000/api/mcp/info

# List all tools
curl http://localhost:9000/api/mcp/tools

# Execute a tool
curl -X POST http://localhost:9000/api/mcp/tools/add_two_numbers/execute \
  -H "Content-Type: application/json" \
  -d '{"a": 15, "b": 27}'
```

## Expected Response
```json
{
  "result": 42,
  "tool": "add_two_numbers",
  "status": "success"
}
```

## Stop the Server
```bash
docker-compose down
```

## Architecture Comparison

| Feature | Python (FastMCP) | Java (mcp4j) |
|---------|-----------------|--------------|
| Build Tool | pip | Maven |
| Server | FastMCP | Spring Boot |
| Tools | @mcp.tool | @Tool + LangChain4j |
| Transport | STDIO/HTTP/SSE | REST API |
| Port | 9000 | 9000 |
| Auth | JWT | OAuth2 |

## Available Endpoints

- `GET  /api/mcp/info` - Server information
- `GET  /api/mcp/tools` - List all tools
- `GET  /api/mcp/tools/{domain}` - Tools by domain
- `POST /api/mcp/tools/{toolName}/execute` - Execute a tool
- `GET  /api/mcp/health` - Health check

## Services

1. **BBDemoService** (Domain: demo)
   - `add_two_numbers` - Add two integers
   - `get_user_info` - Get user information

2. **TechSupportService** (Domain: tech_support)
   - `reset_password` - Reset user password
   - `check_system_status` - Check system status

3. **GeneralService** (Domain: general)
   - `get_current_date` - Get current date
   - `format_text` - Format text (uppercase, lowercase, title)
