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
        mcp_names={
            "list_theaters_theaters__get": "get_theaters",
            "create_theater_theaters__post": "create_theater",
            "get_theater_theaters__theater_id__get": "get_theater_by_id",
            "update_theater_theaters__theater_id__put": "update_theater_by_id",
            "delete_theater_theaters__theater_id__delete": "delete_theater_by_id",
            "get_theater_movies_theaters__theater_id__movies_get": "get_theater_movies",
            "create_movie_movies__post": "create_movie",
            "list_movies_movies__get": "get_movies",
            "get_movie_movies__movie_id__get": "get_movie_by_id",
            "update_movie_movies__movie_id__put": "update_movie_by_id",
            "delete_movie_movies__movie_id__delete": "delete_movie_by_id",
        },
        route_maps=[
            RouteMap(
                # methods=["POST", "PUT", "DELETE"],
                tags={"health"},
                # pattern=r"^/health/.*",
                mcp_type=MCPType.EXCLUDE,
            ),
        ],
    )

    logger.info(f"Initialized {mcp_server_settings.name}...")

    return mcp
