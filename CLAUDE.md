# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server for movie catalog information. The project implements **two distinct MCP server architectures** that can be run independently:

1. **Manual MCP Server** (`server.py`): Explicit tool registration with full control over implementation
2. **FastMCP Auto-Generated Server** (`fastmcp_server.py`): Auto-generates MCP tools from OpenAPI specification

Both servers act as proxies to an external RESTful API server.

## Development Setup

**Package Manager**: This project uses `uv` for dependency management and virtual environment handling.

**Python Version**: Requires Python >=3.12

**Install Dependencies**:
```bash
uv sync
```

**Run Servers**:
```bash
# Manual MCP Server (streamable-http transport)
uv run movie-catalog-mcp-server

# Manual MCP Server (stdio transport)
uv run movie-catalog-stdio-mcp-server

# FastMCP Auto-Generated Server
uv run movie-catalog-fastmcp-server

# MCP Inspector (for development/debugging)
uv run mcp dev src/movie_catalog_mcp_server/inspector_run.py
```

## Dual Server Architecture

### 1. Manual MCP Server (`server.py`)

**Purpose**: Explicit control over tool definitions and implementations.

**How it works**:
- Uses `mcp.server.fastmcp.FastMCP` from the MCP SDK
- Tools are manually defined using `@mcp.tool()` decorator
- Each tool requires explicit implementation
- Configured as **stateless HTTP** server
- Uses custom `RestfulAPIClient` for backend API calls

**Key Components**:
- `create_mcp_server()`: Factory function returning configured MCP instance
- Tools: Decorated functions that become MCP tools (e.g., `get_catalog`)
- Settings: Configured via `McpServerSettings` (env prefix: `MCP_`)

**When to use**: When you need custom business logic, data transformation, or fine-grained control over tool behavior.

### 2. FastMCP Auto-Generated Server (`fastmcp_server.py`)

**Purpose**: Automatically generate MCP tools from an existing OpenAPI specification.

**How it works**:
- Uses `fastmcp.FastMCP.from_openapi()` to auto-generate tools
- Fetches OpenAPI spec from backend API at startup
- Creates MCP tools for API endpoints based on `RouteMap` patterns
- Uses `httpx.AsyncClient` for backend API communication

**Key Components**:
- `create_fastmcp_server()`: Factory function that loads OpenAPI spec and creates server
- `RouteMap`: Defines which API routes become MCP tools vs excluded
  - `MCPType.TOOL`: Endpoint becomes an MCP tool
  - `MCPType.EXCLUDE`: Endpoint is ignored
- Pattern matching: Regex patterns determine which HTTP methods/paths are exposed

**Current Configuration**:
```python
route_maps=[
    RouteMap(methods=["GET"], pattern=r"^/api/v1/.*", mcp_type=MCPType.TOOL),
    RouteMap(methods=["POST"], pattern=r"^/api/v1/.*", mcp_type=MCPType.EXCLUDE),
]
```

**When to use**: When you have a well-defined OpenAPI spec and want to quickly expose API endpoints as MCP tools without manual implementation.

## Configuration

### Environment Variables

The project uses `pydantic-settings` for configuration management with `.env` file support.

**MCP Server Settings** (prefix: `MCP_`):
- `MCP_NAME`: Server name (default: "movie-catalog-mcp-server")
- `MCP_HOST`: Host address (default: "0.0.0.0")
- `MCP_PORT`: Server port (default: 8100)

**API Server Settings** (prefix: `API_`):
- `API_SERVER_URL`: Backend API base URL (default: "http://localhost:8000/")
- `API_ROOT_PATH`: API root path (default: "/api/v1")
- `API_OPENAPI_PATH`: OpenAPI spec path (default: "/openapi.json")

### Settings Classes

Located in `setting.py`:
- `McpServerSettings`: MCP server configuration
- `ApiServerSettings`: External API configuration with computed properties:
  - `server_base_url`: Full base URL for API calls
  - `openapi_url`: Complete URL for fetching OpenAPI spec

## HTTP Client Architecture

The `http_client.py` module provides `RestfulAPIClient`, a comprehensive async HTTP client for RESTful API interactions.

**Features**:
- Async/await support using `httpx.AsyncClient`
- Automatic JSON serialization/deserialization
- Authentication support (API key, Bearer token)
- Context manager pattern for resource management
- Full HTTP method coverage (GET, POST, PUT, PATCH, DELETE)
- Automatic error handling with `raise_for_status()`

**Factory Function**:
```python
create_client(base_url, api_key=None, bearer_token=None, **kwargs) -> RestfulAPIClient
```

**Usage Pattern**:
```python
client = create_client("http://api.example.com")
result = await client.get("/endpoint", params={"key": "value"})
```

## Entry Points

Defined in `pyproject.toml`:
- `movie-catalog-mcp-server`: Manual server with streamable-http transport
- `movie-catalog-fastmcp-server`: FastMCP auto-generated server
- `movie-catalog-stdio-mcp-server`: Manual server with stdio transport

All entry points are defined in `__init__.py`:
- `main()`: Runs manual MCP server (streamable-http)
- `stdio_main()`: Runs manual MCP server (stdio)
- `fastmcp_main()`: Runs FastMCP auto-generated server

## Transport Modes

**streamable-http**: HTTP-based transport for client connections (supports SSE streaming)
**stdio**: Standard input/output transport for local MCP client integration

## Adding New Tools (Manual Server)

When adding tools to the manual server (`server.py`):

```python
@mcp.tool(
    name="tool_name",
    description="Clear description for MCP clients",
    structured_output=True,  # Optional: enables structured data return
)
async def tool_name(param: str, optional_param: str = "default") -> CallToolResult:
    """Docstring for internal documentation."""
    try:
        result = await http_client.get(f"{api_server_settings.root_path}/endpoint")
        return CallToolResult(
            content=[TextContent(type="text", text=f"{result}")],
            structuredContent=result,  # If structured_output=True
        )
    except Exception as e:
        logger.error(f"Error in tool_name: {e}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {e}")],
        )
```

## Modifying FastMCP Routes

To control which API endpoints become MCP tools in `fastmcp_server.py`:

1. **Add new route patterns** to `route_maps` list
2. **Use regex patterns** to match API paths
3. **Specify HTTP methods** to filter by verb
4. **Choose MCP type**: `MCPType.TOOL` (expose) or `MCPType.EXCLUDE` (hide)

Example:
```python
RouteMap(methods=["GET", "POST"], pattern=r"^/api/v2/movies/.*", mcp_type=MCPType.TOOL)
```

## Logging Configuration

Structured logging is configured in `__init__.py`:
- Format: `[timestamp] [level] [module:function:line] - message`
- Handler: StreamHandler (stdout)
- Level: INFO

All modules use `logging.getLogger(__name__)` for proper namespace separation.

## Development Workflow

1. **Backend API Required**: Both server implementations expect an external RESTful API running (default: `http://localhost:8000`)
2. **OpenAPI Spec Required** (FastMCP only): FastMCP server fetches the spec at startup
3. **Tool Testing**: Use MCP Inspector for interactive tool testing during development
4. **Environment Configuration**: Use `.env` file for local development settings

## Key Architectural Decisions

- **Stateless Design**: Both servers are stateless (no session persistence)
- **Async First**: All I/O operations use async/await patterns
- **Separation of Concerns**: Server logic, HTTP client, and settings are decoupled
- **Configuration via Environment**: All runtime configuration externalized to env vars
- **Type Safety**: Pydantic models for settings validation
