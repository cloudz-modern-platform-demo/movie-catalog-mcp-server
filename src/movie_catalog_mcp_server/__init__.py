"""Entry point for the movie catalog MCP server."""

import logging
import logging.config


from movie_catalog_mcp_server.fastmcp_server import create_fastmcp_server
from movie_catalog_mcp_server.server import create_mcp_server
from movie_catalog_mcp_server.setting import logger_settings

# logging.config.fileConfig(logger_settings.config_file, disable_existing_loggers=False)
# logging.getLogger("appLogger").setLevel(logger_settings.level)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s.%(msecs)d] [%(levelname)s] [%(name)s] [%(threadName)s:%(thread)d] [%(module)s:%(funcName)s:%(lineno)d] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)


def main() -> None:
    server = create_mcp_server()
    server.run(transport="streamable-http")


def fastmcp_main() -> None:
    server = create_fastmcp_server()
    server.run(transport="streamable-http")


def stdio_main() -> None:
    server = create_mcp_server()
    server.run(transport="stdio")


# mcp = create_mcp_server()
