"""Simple Docker test - verifies container setup without API calls."""

import sys
print("\n" + "="*60)
print("🧪 Docker Container Test - Agent Template")
print("="*60 + "\n")

# Test 1: Check imports
print("📦 Test 1: Checking imports...")
try:
    from agent import MCPAgent
    from mcp_client import MCPClient
    from config import settings
    from memory import MongoMemory
    print("✅ All imports successful\n")
except Exception as e:
    print(f"❌ Import failed: {e}\n")
    sys.exit(1)

# Test 2: Check MongoDB connection
print("📦 Test 2: Checking MongoDB connection...")
try:
    import os
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://admin:admin123@agent-memory-mongodb:27017/")
    memory = MongoMemory(mongo_uri)
    print(f"✅ MongoDB connected: {mongo_uri}\n")
    
    # Test save interaction
    memory.save_interaction(
        session_id="docker_test",
        role="system",
        content="Docker container test",
        metadata={"test": True}
    )
    print("✅ MongoDB interaction saved\n")
    
except Exception as e:
    print(f"❌ MongoDB test failed: {e}\n")
    sys.exit(1)

# Test 3: Check MCP client
print("📦 Test 3: Checking MCP client...")
try:
    mcp_url = os.getenv("MCP_SERVER_URL", "http://mcp_server-mcp-server-1:9000/mcp")
    print(f"✅ MCP client class available (would connect to {mcp_url})\n")
except Exception as e:
    print(f"❌ MCP client test failed: {e}\n")
    sys.exit(1)

print("="*60)
print("✅ All Docker container tests passed!")
print("="*60 + "\n")

print("📋 Container Info:")
print(f"  - Python modules: ✅ Loaded")
print(f"  - MongoDB: ✅ Connected")
print(f"  - MCP Client: ✅ Available")
print("\n🎉 Docker container is properly configured!\n")
