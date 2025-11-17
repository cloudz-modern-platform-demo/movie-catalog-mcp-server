"""Base settings for AI Agent Studio."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class McpServerSettings(BaseSettings):
    """Settings for MCP Server."""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_prefix="MCP_", env_file=".env", extra="ignore"
    )
    name: str = "movie-catalog-mcp-server"
    host: str = "0.0.0.0"
    port: int = 8100


mcp_server_settings = McpServerSettings()


class ApiServerSettings(BaseSettings):
    """Settings for API Server."""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_prefix="API_", env_file=".env", extra="ignore"
    )
    server_url: str = "http://localhost:8000"
    root_path: str = "/api/v1"
    openapi_path: str = "/openapi.json"

    @property
    def server_base_url(self) -> str:
        """Get the base URL for the API server."""
        return f"{self.server_url}{self.root_path}"

    @property
    def openapi_url(self) -> str:
        """Get the full URL for the OpenAPI specification."""
        return f"{self.server_url}{self.openapi_path}"


api_server_settings = ApiServerSettings()
