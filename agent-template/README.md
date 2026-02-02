# Agent Template

LangChain-based agent template with MCP server integration.

## Features

- **MCP Server Integration**: Connects to multiple MCP servers for tools
- **MongoDB Memory**: Persistent memory using MongoDB
- **Flexible Architecture**: Easy to customize for specific use cases
- **Async Support**: Built with async/await for performance

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
MONGODB_URI=mongodb://admin:admin123@localhost:27017/agent_memory?authSource=admin
AGENT_NAME=my_agent
```

## Usage

```python
from agent import MCPAgent

# Initialize agent with MCP servers
agent = MCPAgent(
    name="data_analyst",
    mcp_servers=[
        "http://localhost:9000/mcp"
    ],
    mongo_uri="mongodb://admin:admin123@localhost:27017/agent_memory?authSource=admin"
)

# Run a task
result = await agent.run(
    task="Analyze the data and provide insights",
    session_id="session_123"
)

print(result['output'])
```

## MCP Server Configuration

The agent expects MCP servers to be provided as a list of URLs:

```python
mcp_servers = [
    "http://localhost:9000/mcp",  # Main MCP server
    "http://localhost:9001/mcp"   # Additional server
]
```

## Architecture

```
┌─────────────┐
│   Agent     │
└──────┬──────┘
       │
       ├─────────┐
       │         │
   ┌───▼───┐ ┌──▼──────┐
   │  MCP  │ │ MongoDB │
   │Servers│ │ Memory  │
   └───────┘ └─────────┘
```
