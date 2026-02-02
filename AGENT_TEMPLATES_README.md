# 🤖 Multi-Agent System with MCP Integration

Complete template system for building AI agents that integrate with Model Context Protocol (MCP) servers using LangChain and LangGraph.

## 📁 Project Structure

```
.
├── memory/                      # MongoDB memory service
│   ├── docker-compose.yml       # MongoDB + Mongo Express
│   └── README.md
│
├── orchestrator-agent/          # Orchestrator template
│   ├── orchestrator.py          # Main orchestrator with LangGraph
│   ├── config.py                # Configuration management
│   ├── memory.py                # MongoDB memory interface
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment template
│   ├── README.md                # Documentation
│   └── test_orchestrator.py    # Test script
│
├── agent-template/              # MCP agent template
│   ├── agent.py                 # Main agent with MCP integration
│   ├── mcp_client.py            # MCP protocol client
│   ├── config.py                # Configuration management
│   ├── memory.py                # MongoDB memory interface
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment template
│   ├── README.md                # Documentation
│   └── test_agent.py            # Test script
│
└── test_integration.py          # Full integration tests
```

## 🚀 Quick Start

### 1. Start Memory Service

```bash
cd memory
docker-compose up -d
```

This starts:
- **MongoDB** on `localhost:27017`
- **Mongo Express UI** on `http://localhost:8081`

### 2. Configure Orchestrator

```bash
cd orchestrator-agent
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
pip install -r requirements.txt
```

### 3. Configure Agent Template

```bash
cd agent-template
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
pip install -r requirements.txt
```

### 4. Start Your MCP Server

Make sure your MCP server is running. For example:

```bash
# Python MCP server
cd Multi-Agent-Custom-Automation-Engine-Solution-Accelerator/src/mcp_server
docker-compose up -d
```

Or:

```bash
# Java mcp4j server
cd mcp4j
docker-compose up -d
```

## 🧪 Testing

### Test Orchestrator

```bash
cd orchestrator-agent
python test_orchestrator.py
```

### Test MCP Agent

```bash
cd agent-template
python test_agent.py
```

### Integration Test

```bash
python test_integration.py
```

## 🏗️ Architecture

### Orchestrator Agent

The orchestrator uses **LangGraph** for workflow management with 5 nodes:

```
┌─────────────┐
│ Analyze Task│
└──────┬──────┘
       ↓
┌─────────────┐
│ Create Plan │
└──────┬──────┘
       ↓
┌─────────────┐
│   Delegate  │
└──────┬──────┘
       ↓
┌─────────────┐
│  Aggregate  │
└──────┬──────┘
       ↓
┌─────────────┐
│  Finalize   │
└─────────────┘
```

**Features:**
- ✅ Multi-agent coordination
- ✅ Task decomposition
- ✅ Result aggregation
- ✅ MongoDB memory persistence
- ✅ Session management

### MCP Agent

The MCP agent integrates with Model Context Protocol servers:

```
┌─────────────┐
│  MCP Agent  │
└──────┬──────┘
       │
       ├─→ MCP Server 1 (Tools)
       ├─→ MCP Server 2 (Tools)
       └─→ MCP Server N (Tools)
       │
       ↓
┌─────────────┐
│   MongoDB   │
│   Memory    │
└─────────────┘
```

**Features:**
- ✅ Multiple MCP server connections
- ✅ Dynamic tool loading
- ✅ LangChain integration
- ✅ MongoDB memory
- ✅ Session persistence

## 📚 Usage Examples

### Example 1: Simple MCP Agent

```python
from agent import MCPAgent
import asyncio

async def main():
    # Create agent with MCP servers
    agent = MCPAgent(
        name="my_agent",
        mcp_servers=[
            "http://localhost:9000/mcp",
            "http://localhost:9001/mcp"
        ]
    )
    
    # Run a task
    result = await agent.run(
        task="Add 15 and 27",
        session_id="demo_session"
    )
    
    print(result['output'])

asyncio.run(main())
```

### Example 2: Orchestrator with Agents

```python
from orchestrator import OrchestratorAgent
import asyncio

async def main():
    # Create orchestrator
    orchestrator = OrchestratorAgent()
    
    # Complex task
    result = await orchestrator.run(
        task="Calculate 50+30, check system status, and format result"
    )
    
    print(result['final_output'])

asyncio.run(main())
```

### Example 3: Agent with Memory

```python
from agent import MCPAgent
import asyncio

async def main():
    agent = MCPAgent(
        name="memory_agent",
        mcp_servers=["http://localhost:9000/mcp"]
    )
    
    session_id = "my_session"
    
    # First interaction
    result1 = await agent.run(
        task="Calculate 10 + 20",
        session_id=session_id
    )
    
    # Second interaction (has context)
    result2 = await agent.run(
        task="Double the previous result",
        session_id=session_id
    )
    
    # Check history
    history = agent.memory.get_session_history(session_id)
    print(f"History: {len(history)} interactions")

asyncio.run(main())
```

## 🔧 Configuration

### Environment Variables

Both orchestrator and agent templates use the same environment variables:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-...

# MongoDB Configuration
MONGODB_URI=mongodb://admin:admin123@localhost:27017/

# Logging
LOG_LEVEL=INFO
```

### MongoDB Access

- **Connection URI**: `mongodb://admin:admin123@localhost:27017/`
- **Database**: `agent_memory`
- **Collections**:
  - `interactions`: Message history
  - `sessions`: Session metadata

### Mongo Express UI

Access the web interface at `http://localhost:8081`:
- Username: `admin`
- Password: `admin123`

## 🛠️ Customization

### Adding Custom Tools to Agents

The agent automatically loads tools from MCP servers. To add custom tools:

```python
from langchain_core.tools import Tool

# In agent.py, after loading MCP tools:
custom_tool = Tool(
    name="my_custom_tool",
    description="Does something custom",
    func=lambda x: f"Custom result: {x}"
)

self.tools.append(custom_tool)
```

### Customizing Orchestrator Workflow

Modify the LangGraph workflow in `orchestrator.py`:

```python
# Add a new node
def my_custom_node(state: OrchestratorState) -> OrchestratorState:
    # Your logic here
    return state

# Add to workflow
workflow.add_node("custom", my_custom_node)
workflow.add_edge("plan", "custom")
workflow.add_edge("custom", "delegate")
```

### Custom Memory Storage

To use a different storage backend, implement the same interface as `MongoMemory`:

```python
class CustomMemory:
    def save_interaction(self, session_id, role, content, metadata):
        pass
    
    def get_session_history(self, session_id, limit):
        pass
```

## 🐛 Troubleshooting

### MongoDB Connection Error

```bash
# Check MongoDB is running
docker ps | grep mongo

# Restart MongoDB
cd memory
docker-compose restart
```

### MCP Server Not Responding

```bash
# Check MCP server is running
curl http://localhost:9000/mcp

# Check logs
docker logs <mcp-container-name>
```

### Tool Loading Fails

- Verify MCP server URL is correct
- Check MCP server implements `tools/list` endpoint
- Review agent logs for detailed errors

### Memory Not Persisting

- Check MongoDB connection string in `.env`
- Verify MongoDB container is healthy: `docker ps`
- Check Mongo Express UI to see if data is being saved

## 📊 Monitoring

### View Agent Activity

Access Mongo Express at `http://localhost:8081`:

1. Navigate to `agent_memory` database
2. View `interactions` collection for message history
3. View `sessions` collection for session metadata

### Logs

Both templates use Python logging:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

Set `LOG_LEVEL=DEBUG` in `.env` for detailed logs.

## 🔒 Security

### Production Deployment

For production use:

1. **Change MongoDB credentials**:
   ```yaml
   # In memory/docker-compose.yml
   MONGO_INITDB_ROOT_USERNAME: your_username
   MONGO_INITDB_ROOT_PASSWORD: your_strong_password
   ```

2. **Use secrets management**:
   ```bash
   # Don't commit .env files
   echo ".env" >> .gitignore
   ```

3. **Enable MongoDB authentication**:
   ```python
   MONGODB_URI=mongodb://user:pass@host:port/?authSource=admin
   ```

4. **Use HTTPS for MCP servers**:
   ```python
   mcp_servers=["https://secure-server.com/mcp"]
   ```

## 🤝 Contributing

This is a template system for AI engineers. Feel free to:

- Add more agent templates
- Improve the orchestration workflow
- Add new MCP server integrations
- Enhance memory management

## 📄 License

MIT License - feel free to use these templates in your projects!

## 🙏 Credits

Built with:
- **LangChain**: Agent framework
- **LangGraph**: Workflow orchestration
- **FastMCP**: Model Context Protocol
- **MongoDB**: Memory persistence
- **OpenAI**: Language models

---

**Happy Building! 🚀**

For questions or issues, please refer to individual component READMEs:
- [Orchestrator README](orchestrator-agent/README.md)
- [Agent Template README](agent-template/README.md)
- [Memory README](memory/README.md)
