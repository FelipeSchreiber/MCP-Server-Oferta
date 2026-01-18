"""
FastMCP Client Template for ASGI Server
Connects to FastMCP HTTP server and uses OpenAI to interact with tools/resources
"""
import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SERVER_URL = "http://127.0.0.1:8000/mcp"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# MCP Session management
session_id = None


def parse_sse_response(text: str) -> dict:
    """Parse Server-Sent Events response format"""
    for line in text.split('\n'):
        if line.startswith('data: '):
            return json.loads(line[6:])
    return {}


def initialize_mcp_session() -> str:
    """Initialize MCP session and return session ID"""
    global session_id
    
    r = requests.post(SERVER_URL, json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "fastmcp-client", "version": "1.0.0"}
        }
    }, headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    })
    
    data = parse_sse_response(r.text)
    session_id = r.headers.get('mcp-session-id')
    print(f"Session ID: {session_id}")
    return session_id


def retrieve_mcp_tools() -> list:
    """Retrieve available tools from MCP server"""
    r = requests.post(SERVER_URL, json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {}
    }, headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "mcp-session-id": session_id
    })
    
    data = parse_sse_response(r.text)
    tools = data.get('result', {}).get('tools', [])
    
    # Convert to OpenAI function format
    openai_tools = []
    for tool in tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool['name'],
                "description": tool.get('description', ''),
                "parameters": tool.get('inputSchema', {})
            }
        })
    
    return openai_tools


def retrieve_mcp_resources() -> list:
    """Retrieve available resources from MCP server"""
    r = requests.post(SERVER_URL, json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "resources/list",
        "params": {}
    }, headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "mcp-session-id": session_id
    })
    
    data = parse_sse_response(r.text)
    resources = data.get('result', {}).get('resources', [])
    
    # Convert resources to OpenAI functions
    openai_resources = []
    for resource in resources:
        openai_resources.append({
            "type": "function",
            "function": {
                "name": f"resource_{resource['name'].replace('://', '_').replace('/', '_')}",
                "description": f"Read resource: {resource.get('description', resource['uri'])}",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        })
    
    return openai_resources


def call_mcp_tool(tool_name: str, arguments: dict) -> dict:
    """Call an MCP tool"""
    r = requests.post(SERVER_URL, json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }, headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "mcp-session-id": session_id
    })
    
    return parse_sse_response(r.text).get('result', {})


def call_mcp_resource(uri: str) -> dict:
    """Read an MCP resource"""
    r = requests.post(SERVER_URL, json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "resources/read",
        "params": {"uri": uri}
    }, headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "mcp-session-id": session_id
    })
    
    return parse_sse_response(r.text).get('result', {})


def main():
    """Main client loop with OpenAI integration"""
    print(f"Connecting to MCP server at {SERVER_URL}...")
    
    # Initialize MCP session
    initialize_mcp_session()
    
    # Retrieve available tools and resources
    print("\nRetrieving available tools and resources...")
    mcp_tools = retrieve_mcp_tools()
    mcp_resources = retrieve_mcp_resources()
    all_tools = mcp_tools + mcp_resources
    
    print(f"Found {len(mcp_tools)} tools and {len(mcp_resources)} resources")
    print(f"Tools: {[t['function']['name'] for t in mcp_tools]}")
    print(f"Resources: {[r['function']['name'] for r in mcp_resources]}")
    
    # Chat loop with OpenAI
    messages = [
        {"role": "system", "content": "You are a helpful assistant that can use MCP tools and resources to help users."}
    ]
    
    print("\n" + "="*50)
    print("Chat with AI (type 'quit' to exit)")
    print("="*50 + "\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if not user_input:
            continue
        
        messages.append({"role": "user", "content": user_input})
        
        # Call OpenAI with available tools
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=all_tools,
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
        
        # Handle tool calls
        if assistant_message.tool_calls:
            messages.append(assistant_message)
            
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"\n🔧 Calling: {function_name}({function_args})")
                
                # Route to tool or resource
                if function_name.startswith("resource_"):
                    # Extract original resource URI from function name
                    if "config_app_config" in function_name:
                        result = call_mcp_resource("config://app_config")
                    else:
                        result = {"error": "Unknown resource"}
                elif function_name == "get_user_info":
                    # Client-side approval for sensitive data
                    user_id = function_args.get("user_id", "unknown")
                    print(f"\n🔒 APPROVAL REQUIRED: Access user {user_id} information?")
                    
                    while True:
                        choice = input("   [y]es or [n]o? ").strip().lower()
                        if choice in ['y', 'yes']:
                            print("✅ APPROVED - Retrieving data...")
                            result = call_mcp_tool(function_name, function_args)
                            
                            # Display result
                            if 'content' in result and result['content']:
                                try:
                                    content_text = result['content'][0].get('text', '')
                                    data = json.loads(content_text) if content_text else result
                                    print(f"   Retrieved: {json.dumps(data, indent=6)}")
                                except:
                                    pass
                            break
                        elif choice in ['n', 'no']:
                            print("❌ DECLINED")
                            result = {
                                "content": [{
                                    "type": "text",
                                    "text": json.dumps({"error": "Access denied by user"})
                                }]
                            }
                            break
                        else:
                            print("   Invalid input. Please enter 'y' or 'n'")
                else:
                    # Call tool - approval will be handled by server if needed
                    result = call_mcp_tool(function_name, function_args)
                    
                    # Display result
                    if 'content' in result and result['content']:
                        try:
                            content_text = result['content'][0].get('text', '')
                            data = json.loads(content_text) if content_text else result
                            print(f"   Result: {json.dumps(data, indent=6)}")
                        except:
                            print(f"   Result: {result}")
                
                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
            
            # Get final response after tool calls
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            assistant_message = response.choices[0].message
        
        messages.append(assistant_message)
        print(f"\nAssistant: {assistant_message.content}\n")


if __name__ == "__main__":
    main()
