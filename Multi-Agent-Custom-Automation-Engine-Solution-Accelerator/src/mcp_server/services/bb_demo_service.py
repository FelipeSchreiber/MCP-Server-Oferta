"""Demo Service - Template tools for BB Internal Developer Platform."""

from fastmcp import FastMCP, Context
from core.factory import MCPToolBase, Domain


class BBDemoService(MCPToolBase):
    """Demo service with template tools for BB Internal Developer Platform."""

    def __init__(self):
        super().__init__(Domain.DEMO)
        self._tool_count = 2  # add_two_numbers, get_user_info

    @property
    def tool_count(self) -> int:
        """Return the number of tools provided by this service."""
        return self._tool_count

    def register_tools(self, mcp: FastMCP) -> None:
        """Register demo tools and resources with the FastMCP server."""

        # Tool: Basic arithmetic operation
        @mcp.tool(
            name="add_two_numbers",
            description="Adds two integer numbers together.",
            tags={self.domain.value, "math", "addition"},
            meta={"version": "1.0", "author": "bb-platform"},
        )
        def add(a: int, b: int) -> int:
            """Adds two integer numbers together."""
            return a + b

        # Tool: Access user information with approval
        @mcp.tool(
            name="get_user_info",
            description=(
                "Retrieves user information by user_id. Returns user profile "
                "including id, name, and status. This tool accesses sensitive "
                "user data."
            ),
            tags={self.domain.value, "user", "profile", "info"},
            meta={"version": "1.0", "author": "bb-platform"},
        )
        async def get_user_info(ctx: Context, user_id: int) -> dict:
            """Retrieves user information by user_id with approval."""
            result = await ctx.elicit("Choose an action")

            if result.action == "accept":
                return {
                    "id": user_id,
                    "name": f"User {user_id}",
                    "status": "active",
                    "cpf": f"000.000.000-0{user_id}",
                    "email": f"user{user_id}@bb.com.br",
                }
            elif result.action == "decline":
                return {"message": "Declined!"}
            else:
                return {"message": "Cancelled!"}

        # Resource: Application configuration
        @mcp.resource(
            "config://app_config",
            name="get_config",
            description="Provides the application configuration.",
            tags={self.domain.value, "config", "settings"},
            mime_type="application/json",
            meta={"version": "1.0", "author": "bb-platform"},
        )
        def get_config() -> dict:
            """Provides the application configuration."""
            return {"theme": "dark", "version": "1.2"}

        # Resource Template: User telephone with path parameters
        @mcp.resource(
            "users://{user_id}/telephone",
            name="get_user_telephone",
            description="Retrieves a user's telephone by ID.",
            mime_type="application/json",
            tags={self.domain.value, "user", "telephone"},
            meta={"version": "1.0", "author": "bb-platform"},
        )
        def get_user_telephone(user_id: int) -> dict:
            """Retrieves a user's telephone by ID."""
            return {
                "id": user_id,
                "name": f"User {user_id}",
                "telephone": f"+55-61-3000-{user_id:04d}",
            }

        # Prompt: Data analysis template
        @mcp.prompt
        def analyze_data(data_points: list[float]) -> str:
            """Creates a prompt asking for analysis of numerical data."""
            formatted_data = ", ".join(str(point) for point in data_points)
            return f"Please analyze these data points: {formatted_data}"
