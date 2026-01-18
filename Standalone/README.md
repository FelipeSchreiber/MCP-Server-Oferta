## Build
```bash
docker build -t my_server .
```

## Run
```bash
docker run -d -p 8000:8000 --env-file ../.env my_server
```

## Generate mcp.json for Local Docker
```bash
mkdir -p .vscode && cat > .vscode/mcp.json << 'EOF'
{
  "servers": {
    "DemoServer": {
      "url": "http://127.0.0.1:8000/mcp",
      "type": "http"
    }
  },
	"inputs": []
}
EOF
```

## Generate server.json (for STDIO mode)
```bash
fastmcp install mcp-json fastmcp_server_template.py > mcp.json
```