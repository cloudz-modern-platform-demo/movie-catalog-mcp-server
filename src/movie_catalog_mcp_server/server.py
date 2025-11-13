"""Create a MCP server for movie catalog information."""

import logging

from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent

from movie_catalog_mcp_server.http_client import create_client
from movie_catalog_mcp_server.setting import api_server_settings, mcp_server_settings

logger = logging.getLogger(__name__)


def create_mcp_server():
    mcp = FastMCP(
        "Movie Catalog MCP Server",
        instructions="This is a server that provides information about movies.",
        stateless_http=True,
        host=mcp_server_settings.host,
        port=mcp_server_settings.port,
    )

    client = create_client(api_server_settings.server_url)

    # Add a simple tool to demonstrate the server
    @mcp.tool()
    async def hello(name: str = "World") -> CallToolResult:
        """Greet someone by name."""
        try:
            result = await client.get(
                f"{api_server_settings.root_path}/hello", params={"name": name}
            )

            return CallToolResult(
                content=[TextContent(type="text", text=f"{result}")],
                structuredContent=result,
            )
        except Exception as e:
            logger.error(f"Error greeting {name}: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error: {e}")],
            )

    logger.info(f"Initialized {mcp_server_settings.name}...")

    return mcp
