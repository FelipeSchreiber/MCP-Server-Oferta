"""
BB MCP Server - FastMCP server with organized tools and services.
"""

import argparse
import logging

from config.settings import config
from core.factory import MCPToolFactory
from fastmcp.server.auth.providers.jwt import JWTVerifier
from services.bb_demo_service import BBDemoService
from services.demo_tech_support_service import TechSupportService
from services.demo_general_service import GeneralService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global factory instance
factory = MCPToolFactory()

# Initialize services
factory.register_service(BBDemoService())
factory.register_service(TechSupportService())
factory.register_service(GeneralService())


def create_fastmcp_server():
    """Create and configure FastMCP server."""
    try:
        # Create authentication provider if enabled
        auth = None
        if config.enable_auth:
            auth_config = {
                "jwks_uri": config.jwks_uri,
                "issuer": config.issuer,
                "audience": config.audience,
            }
            if all(auth_config.values()):
                auth = JWTVerifier(
                    jwks_uri=auth_config["jwks_uri"],
                    issuer=auth_config["issuer"],
                    algorithm="RS256",
                    audience=auth_config["audience"],
                )

        # Create MCP server
        mcp_server = factory.create_mcp_server(
            name=config.server_name,
            auth=auth,
        )

        logger.info("✅ FastMCP server created successfully")
        return mcp_server

    except ImportError:
        logger.warning(
            "⚠️  FastMCP not available. Install with: pip install fastmcp"
        )
        return None



# Create FastMCP server instance for fastmcp run command
mcp = create_fastmcp_server()

# Add /health endpoint if mcp is available
if mcp:
    try:
        from starlette.requests import Request
        from starlette.responses import PlainTextResponse
        
        @mcp.custom_route("/health", methods=["GET"])
        async def health_check(request: Request) -> PlainTextResponse:
            return PlainTextResponse("OK")
    except ImportError:
        pass


def log_server_info():
    """Log server initialization info."""
    if not mcp:
        logger.error("❌ FastMCP server not available")
        return

    summary = factory.get_tool_summary()
    logger.info(f"🚀 {config.server_name} initialized")
    logger.info(f"📊 Total services: {summary['total_services']}")
    logger.info(f"🔧 Total tools: {summary['total_tools']}")
    auth_status = "Enabled" if config.enable_auth else "Disabled"
    logger.info(f"🔐 Authentication: {auth_status}")

    for domain, info in summary["services"].items():
        logger.info(
            f"   📁 {domain}: {info['tool_count']} tools ({info['class_name']})"
        )


def run_server(
    transport: str = "stdio",
    host: str = "127.0.0.1",
    port: int = 9000,
    **kwargs,
):
    """Run the FastMCP server with specified transport."""
    if not mcp:
        logger.error("❌ Cannot start FastMCP server - not available")
        return

    log_server_info()

    logger.info(f"🤖 Starting FastMCP server with {transport} transport")
    if transport in ["http", "streamable-http", "sse"]:
        logger.info(
            "🌐 Server will be available at: "
            f"http://{host}:{port}/mcp/"
        )
        mcp.run(transport=transport, host=host, port=port, **kwargs)
    else:
        # For STDIO transport, only pass kwargs that are supported
        stdio_kwargs = {
            k: v for k, v in kwargs.items() if k not in ["log_level"]
        }
        mcp.run(transport=transport, **stdio_kwargs)


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="BB Internal Developer Platform - MCP Server"
    )
    parser.add_argument(
        "--transport",
        "-t",
        choices=["stdio", "http", "streamable-http", "sse"],
        default="stdio",
        help="Transport protocol (default: stdio)",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to for HTTP transport (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=9000,
        help="Port to bind to for HTTP transport (default: 9000)",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug mode"
    )
    parser.add_argument(
        "--no-auth", action="store_true", help="Disable authentication"
    )

    args = parser.parse_args()

    # Override config with command line arguments
    if args.debug:
        import os

        os.environ["MCP_DEBUG"] = "true"
        config.debug = True

    if args.no_auth:
        import os

        os.environ["MCP_ENABLE_AUTH"] = "false"
        config.enable_auth = False

    # Print startup info
    print("🚀 Starting BB MCP Server - Internal Developer Platform")
    print(f"📋 Transport: {args.transport.upper()}")
    print(f"🔧 Debug: {config.debug}")
    print(f"🔐 Auth: {'Enabled' if config.enable_auth else 'Disabled'}")
    if args.transport in ["http", "streamable-http", "sse"]:
        print(f"🌐 Host: {args.host}")
        print(f"🌐 Port: {args.port}")
    print("-" * 50)

    # Run the server
    run_server(
        transport=args.transport,
        host=args.host,
        port=args.port,
        log_level="debug" if args.debug else "info",
    )


if __name__ == "__main__":
    main()
