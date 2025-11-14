"""Create a FastMCP server for movie catalog information."""

import logging
from fastmcp.server.openapi import MCPType, RouteMap
import httpx

from fastmcp import FastMCP
from movie_catalog_mcp_server.setting import api_server_settings, mcp_server_settings

logger = logging.getLogger(__name__)


def create_fastmcp_server() -> FastMCP:
    """Create a FastMCP server for movie catalog information."""

    # Create an HTTP client for your API
    client = httpx.AsyncClient(base_url=api_server_settings.server_url)

    # Load your OpenAPI spec
    openapi_spec = httpx.get(api_server_settings.openapi_url).json()

    # Create the MCP server
    mcp = FastMCP.from_openapi(
        openapi_spec=openapi_spec,
        client=client,
        name="Movie Catalog MCP Server",
        # mcp_names={
        #     "hello_api_v1_hello_get": "get_catalog",
        #     "hello_post_api_v1_hello_post": "create_post",
        #     "hello_put_api_v1_hello": "update_post",
        #     "hello_delete_api_v1_hello": "delete_post",
        # },
        route_maps=[
            RouteMap(methods=["GET"], pattern=r"^/api/v1/.*", mcp_type=MCPType.TOOL),
            RouteMap(
                methods=["POST"],
                pattern=r"^/api/v1/.*",
                mcp_type=MCPType.EXCLUDE,
            ),
        ],
    )

    logger.info(f"Initialized {mcp_server_settings.name}...")

    return mcp
