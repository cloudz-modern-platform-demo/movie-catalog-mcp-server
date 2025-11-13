"""Create a FastMCP server for movie catalog information."""

import httpx

from fastmcp import FastMCP
from movie_catalog_mcp_server.setting import api_server_settings, mcp_server_settings


def create_fastmcp_server():
    # Create an HTTP client for your API
    client = httpx.AsyncClient(base_url=api_server_settings.server_url)

    # Load your OpenAPI spec
    openapi_spec = httpx.get(api_server_settings.openapi_url).json()

    # Create the MCP server
    mcp = FastMCP.from_openapi(
        openapi_spec=openapi_spec,
        client=client,
        name="Movie Catalog MCP Server",
        host=mcp_server_settings.host,
        port=mcp_server_settings.port,
    )

    return mcp
