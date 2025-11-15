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

    http_client = create_client(api_server_settings.server_url)

    # Add a simple tool to demonstrate the server
    @mcp.tool(
        name="get_theaters",
        description="Get the theaters of movies.",
        structured_output=True,
    )
    async def get_theaters() -> CallToolResult:
        """Get the theaters of movies."""
        try:
            result = await http_client.get("/theaters", params={})

            # Wrap list response in a dictionary for structuredContent
            if isinstance(result, list):
                structured_content = {"theaters": result}
            else:
                structured_content = result

            return CallToolResult(
                content=[TextContent(type="text", text=f"{result}")],
                structuredContent=structured_content,
            )
        except Exception as e:
            logger.error(f"Error getting theaters: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error: {e}")],
            )

    @mcp.tool(
        name="get_theater_by_id",
        description="Get the theater by id.",
        structured_output=True,
    )
    async def get_theater_by_id(theater_id: str) -> CallToolResult:
        """Get the theaters of movies."""
        try:
            result = await http_client.get(f"/theaters/{theater_id}", params={})

            # Wrap list response in a dictionary for structuredContent
            if isinstance(result, list):
                structured_content = {"theaters": result}
            else:
                structured_content = result

            return CallToolResult(
                content=[TextContent(type="text", text=f"{result}")],
                structuredContent=structured_content,
            )
        except Exception as e:
            logger.error(f"Error getting theaters: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error: {e}")],
            )

    logger.info(f"Initialized {mcp_server_settings.name}...")

    return mcp
