# Movie Catalog MCP Server

MCP (Model Context Protocol) server for movie catalog information with dual architecture support.

## Prerequisites

- Python >= 3.12
- uv (Python package manager)

## Installation

Install all project dependencies using `uv`:

```bash
uv sync
```

This will create a virtual environment and install all required packages including:
- FastMCP framework
- MCP SDK
- httpx for async HTTP requests
- pydantic-settings for configuration

## Running the Servers

This project provides **three different server configurations**:

### 1. Manual MCP Server (Streamable HTTP)

Default server with explicit tool registration:

```bash
uv run movie-catalog-mcp-server
```

- **Transport**: Streamable HTTP (supports SSE streaming)
- **Host**: 0.0.0.0
- **Port**: 8100
- **Use Case**: Custom business logic and fine-grained control

### 2. Manual MCP Server (Stdio)

Same as above but using stdio transport for local integration:

```bash
uv run movie-catalog-stdio-mcp-server
```

- **Transport**: Standard input/output
- **Use Case**: Local MCP client integration (e.g., Claude Desktop)

### 3. FastMCP Auto-Generated Server

Automatically generates tools from OpenAPI specification:

```bash
uv run movie-catalog-fastmcp-server
```

- **Transport**: Streamable HTTP
- **Host**: 0.0.0.0
- **Port**: 8100
- **Use Case**: Quick API proxy without manual tool implementation
- **Requires**: Backend API with OpenAPI spec at `http://localhost:8000/openapi.json`

## Development & Testing

### MCP Inspector

Interactive tool for testing and debugging MCP tools during development:

```bash
uv run mcp dev src/movie_catalog_mcp_server/inspector_run.py
```

The inspector provides a web interface to test all registered MCP tools.

## Configuration

Configure the servers using environment variables or a `.env` file:

### MCP Server Settings

```bash
MCP_NAME=movie-catalog-mcp-server  # Server name
MCP_HOST=0.0.0.0                    # Server host
MCP_PORT=8100                       # Server port
```

### Backend API Settings

```bash
API_SERVER_URL=http://localhost:8000/  # Backend API base URL
API_ROOT_PATH=/api/v1                   # API root path
API_OPENAPI_PATH=/openapi.json          # OpenAPI spec path
```

## Quick Start

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Start your backend API** (required):
   ```bash
   # Make sure your movie catalog API is running at http://localhost:8000
   ```

3. **Run the MCP server**:
   ```bash
   # For manual server:
   uv run movie-catalog-mcp-server

   # OR for auto-generated server:
   uv run movie-catalog-fastmcp-server
   ```

4. **Test with MCP Inspector**:
   ```bash
   uv run mcp dev src/movie_catalog_mcp_server/inspector_run.py
   ```

## Architecture

See [CLAUDE.md](./CLAUDE.md) for detailed architecture documentation.