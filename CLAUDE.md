# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server for movie catalog information, built using FastMCP. The server provides a streamable HTTP interface for Claude and other MCP clients to access movie-related functionality.

## Development Setup

**Package Manager**: This project uses `uv` for dependency management and virtual environment handling.

**Python Version**: Requires Python >=3.12

**Install Dependencies**:
```bash
uv sync
```

**Run the Server**:
```bash
uv run src/movie_catalog_mcp_server/server.py
```

**Run Entry Point (Alternative)**:
```bash
uv run movie-catalog-mcp-server
```

## Architecture

### Core Components

**FastMCP Server** (`src/movie_catalog_mcp_server/server.py`):
- Main MCP server implementation using the FastMCP framework
- Configured as a **stateful server** (maintains session state)
- Runs on `0.0.0.0:8100` with streamable HTTP transport
- Tools are defined using the `@mcp.tool()` decorator pattern
- Server instructions: "This is a server that provides information about movies."

**Entry Point** (`src/movie_catalog_mcp_server/__init__.py`):
- Simple console application entry point
- Mapped in `pyproject.toml` as `movie-catalog-mcp-server` command

**HTTP Client** (`src/movie_catalog_mcp_server/http_client.py`):
- Currently a placeholder file (single line)
- Likely intended for outgoing HTTP requests to movie databases/APIs

### MCP Server Configuration

The server uses FastMCP's streamable HTTP transport, which:
- Maintains session state across requests (stateful)
- Supports SSE (Server-Sent Events) streaming with compatible clients
- Allows Claude Desktop and other MCP clients to connect via HTTP

**Alternative configurations** (commented in `server.py`):
- Stateless HTTP: `FastMCP("StatelessServer", stateless_http=True)`
- Stateless JSON response: `FastMCP("StatelessServer", stateless_http=True, json_response=True)`

## Adding New Tools

Tools are the primary way to expose functionality to MCP clients. Follow this pattern:

```python
@mcp.tool()
def tool_name(param: str, optional_param: str = "default") -> str:
    """Clear description of what the tool does."""
    # Implementation
    return result
```

All tools must:
- Have type hints for parameters and return values
- Include a docstring that describes the tool's purpose
- Be decorated with `@mcp.tool()`

## Project Structure

```
movie-catalog-mcp-server/
├── src/movie_catalog_mcp_server/
│   ├── __init__.py          # Entry point
│   ├── server.py            # FastMCP server with tools
│   └── http_client.py       # HTTP client (placeholder)
├── pyproject.toml           # Project metadata and dependencies
├── uv.lock                  # Locked dependencies
└── README.md                # (empty)
```

## Key Dependencies

- **mcp>=1.21.0**: Model Context Protocol SDK with FastMCP framework
- Built with `uv_build>=0.8.17,<0.9.0`

## Testing the Server

Once running, the server will be accessible at:
- **Host**: `0.0.0.0`
- **Port**: `8100`
- **Transport**: streamable-http

Connect from Claude Desktop or other MCP clients using the HTTP endpoint.

## Development Notes

- The project is currently in early stages with placeholder implementations
- The `http_client.py` module is empty and awaiting implementation
- The README.md is empty and needs documentation
- No tests are currently present in the repository
