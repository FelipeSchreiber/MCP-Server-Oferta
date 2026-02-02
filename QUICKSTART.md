# 🚀 Quickstart Guide - Agent Templates

Get started with the AI agent templates in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- Python 3.10+ installed
- OpenAI API key

## Step 1: Services are Already Running ✅

The following services are already started:

```bash
✅ MongoDB (port 27017) - Memory database
✅ Mongo Express (port 8081) - Web UI
✅ MCP Server (port 9000) - Tool server
```

Verify with:
```bash
docker ps | grep -E "mongo|mcp"
```

## Step 2: Set Up Environment

Your `.env` files are already created in both templates:

- `orchestrator-agent/.env`
- `agent-template/.env`

Both contain:
```bash
OPENAI_API_KEY=<your-key>
MONGODB_URI=mongodb://admin:admin123@localhost:27017/
LOG_LEVEL=INFO
```

## Step 3: Install Dependencies

### For Agent Template:
```bash
cd agent-template
pip install -r requirements.txt
```

### For Orchestrator:
```bash
cd orchestrator-agent
pip install -r requirements.txt
```

## Step 4: Test the Agent

```bash
cd agent-template
python test_agent.py
```

Expected output:
```
🧪 Testing MCP Agent
═══════════════════════════════
✅ Agent initialized with 9 tools
📝 Test 1: Calculate 15 + 27
✅ Result: The sum of 15 and 27 is 42
```

## Step 5: Test the Orchestrator

```bash
cd orchestrator-agent
python test_orchestrator.py
```

Expected output:
```
🧪 Testing Orchestrator Agent
═════════════════════════════
📝 Task: Calculate the sum...
✅ Test Results
Final Output: <orchestrated result>
```

## Step 6: Run Integration Test

```bash
cd ..  # Back to root
python test_integration.py
```

This tests the full system: orchestrator coordinating multiple MCP agents.

## Quick Examples

### Example 1: Simple Agent

```python
from agent import MCPAgent
import asyncio

async def main():
    agent = MCPAgent(
        name="my_agent",
        mcp_servers=["http://localhost:9000/mcp"]
    )
    
    result = await agent.run(
        task="Add 10 and 20",
        session_id="demo"
    )
    
    print(result['output'])

asyncio.run(main())
```

### Example 2: Custom Orchestrator

```python
from orchestrator import OrchestratorAgent
import asyncio

async def main():
    orchestrator = OrchestratorAgent()
    
    result = await orchestrator.run(
        task="Your complex task here"
    )
    
    print(result['final_output'])

asyncio.run(main())
```

## View MongoDB Data

Open your browser:
```
http://localhost:8081
```

Login:
- Username: `admin`
- Password: `admin123`

Navigate to `agent_memory` database to see:
- `interactions` - All agent conversations
- `sessions` - Session metadata

## Troubleshooting

### MongoDB Not Running?
```bash
cd memory
docker-compose up -d
```

### MCP Server Not Running?
```bash
cd Multi-Agent-Custom-Automation-Engine-Solution-Accelerator/src/mcp_server
docker-compose up -d
```

### Dependencies Not Installed?
```bash
# For agent
cd agent-template
pip install -r requirements.txt

# For orchestrator
cd orchestrator-agent
pip install -r requirements.txt
```

### OpenAI API Key Not Set?
Edit the `.env` files in both folders:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

## Next Steps

1. **Read the Documentation**:
   - [Main README](AGENT_TEMPLATES_README.md) - Complete guide
   - [Implementation Summary](IMPLEMENTATION_SUMMARY.md) - Technical details

2. **Customize Agents**:
   - Modify prompts in `agent.py`
   - Add custom tools
   - Change workflow in `orchestrator.py`

3. **Add More MCP Servers**:
   - Deploy additional MCP servers
   - Connect agents to multiple servers
   - Build specialized agents

4. **Production Deployment**:
   - Change MongoDB credentials
   - Use secrets management
   - Enable HTTPS
   - Add monitoring

## Architecture Summary

```
┌──────────────┐
│ Orchestrator │ ← LangGraph workflow
└──────┬───────┘
       │
       ↓
┌──────────────┐
│  MCP Agents  │ ← Connect to MCP servers
└──────┬───────┘
       │
       ↓
┌──────────────┐
│   MongoDB    │ ← Memory persistence
└──────────────┘
```

## File Structure

```
agent-template/          # Reusable agent template
  ├── agent.py          # Main agent logic
  ├── mcp_client.py     # MCP protocol client
  ├── config.py         # Configuration
  ├── memory.py         # MongoDB interface
  └── test_agent.py     # Test script

orchestrator-agent/     # Orchestrator template
  ├── orchestrator.py   # LangGraph workflow
  ├── config.py         # Configuration
  ├── memory.py         # MongoDB interface
  └── test_orchestrator.py  # Test script

memory/                 # MongoDB service
  └── docker-compose.yml
```

## Support

- Check [AGENT_TEMPLATES_README.md](AGENT_TEMPLATES_README.md) for detailed docs
- Review [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for technical details
- See individual README files in each folder

---

**You're all set! Start building! 🚀**
