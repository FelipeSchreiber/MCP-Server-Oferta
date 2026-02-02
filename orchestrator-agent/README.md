# Orchestrator Agent Template

LangGraph-based orchestrator agent for multi-agent coordination.

## Features

- **Multi-Agent Coordination**: Orchestrates multiple specialized agents
- **State Management**: Uses MongoDB for persistent state
- **LangGraph Workflow**: Implements complex agent workflows
- **Dynamic Routing**: Routes tasks to appropriate agents

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Set environment variables in `.env`:

```env
OPENAI_API_KEY=your_openai_api_key
MONGODB_URI=mongodb://admin:admin123@localhost:27017/agent_memory?authSource=admin
```

## Usage

```python
from orchestrator import OrchestratorAgent

# Initialize orchestrator
orchestrator = OrchestratorAgent(
    mongo_uri="mongodb://admin:admin123@localhost:27017/agent_memory?authSource=admin"
)

# Run a task
result = await orchestrator.run(
    task="Analyze the sales data and create a report",
    agent_configs=[
        {"name": "analyst", "mcp_servers": ["http://localhost:9000/mcp"]},
        {"name": "writer", "mcp_servers": ["http://localhost:9001/mcp"]}
    ]
)
```

## Architecture

The orchestrator uses LangGraph to create a state machine that:
1. Analyzes the task
2. Plans the workflow
3. Delegates to specialized agents
4. Aggregates results
5. Provides final output
