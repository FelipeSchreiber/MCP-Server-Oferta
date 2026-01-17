from fastmcp import FastMCP

# Initialize the FastMCP server instance
mcp = FastMCP(name="DemoServer")

# É possível filtrar quais ferramentas e recursos são expostos ao LLM
# Usando include_tags e exclude_tags para controle fino
# Exemplo:
# mcp = FastMCP(include_tags={"admin"}, exclude_tags={"deprecated"})

## Tools: Expose functions as tools to the LLM with custom metadata
@mcp.tool(
    name="add_two_numbers",           # Custom tool name for the LLM
    description="Adds two integer numbers together.", # Custom description
    tags={"math", "addition"},      # Optional tags for organization/filtering
    meta={"version": "1.0", "author": "calculator-team"}  
)
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b

## Resource: Expose a resource with custom metadata
@mcp.resource("config://app_config",
    name="get_config",
    description="Provides the application configuration.", 
    tags={"config", "settings"},      
    meta={"version": "1.0", "author": "config-team"}  
)
def get_config() -> dict:
    """Provides the application configuration."""
    return {"theme": "dark", "version": "1.2"}

## Resource Templates: Expose a resource with path parameters
@mcp.resource("users://{user_id}/profile", 
    name="get_user_profile",
    description="Retrieves a user's profile by ID.", 
    tags={"user", "profile"},      
    meta={"version": "1.0", "author": "user-team"}  
)
def get_user_profile(user_id: int) -> dict:
    """Retrieves a user's profile by ID."""
    # The {user_id} in the URI is extracted and passed to this function
    return {"id": user_id, "name": f"User {user_id}", "status": "active"}

## Prompt: Expose a prompt template with dynamic content
@mcp.prompt
def analyze_data(data_points: list[float]) -> str:
    """Creates a prompt asking for analysis of numerical data."""
    formatted_data = ", ".join(str(point) for point in data_points)
    return f"Please analyze these data points: {formatted_data}"

if __name__ == "__main__":
    # This runs the server, defaulting to STDIO transport
    # mcp.run()
    
    # Start an HTTP server on port 8000
    # Use 0.0.0.0 to bind to all interfaces (required for Docker)
    mcp.run(transport="http", host="0.0.0.0", port=8000)