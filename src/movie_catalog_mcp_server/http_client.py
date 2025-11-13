"""
HTTP Client for external RESTful API calls using httpx.
Supports async operations and follows OpenAPI/RESTful conventions.
"""

from typing import Any, Dict
import httpx
from contextlib import asynccontextmanager


class RestfulAPIClient:
    """
    HTTP client for interacting with OpenAPI-based RESTful APIs.

    Features:
    - Async support with httpx.AsyncClient
    - Automatic JSON handling
    - Configurable timeout and retry logic
    - Support for common HTTP methods (GET, POST, PUT, PATCH, DELETE)
    - Authentication support (Bearer token, API key)
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        headers: Dict[str, str] | None = None,
        api_key: str | None = None,
        bearer_token: str | None = None,
    ):
        """
        Initialize the RESTful API client.

        Args:
            base_url: Base URL of the API (e.g., "https://api.example.com")
            timeout: Request timeout in seconds (default: 30.0)
            headers: Additional headers to include in all requests
            api_key: API key for authentication (added as X-API-Key header)
            bearer_token: Bearer token for authentication (added as Authorization header)
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.default_headers = headers or {}

        # Setup authentication headers
        if api_key:
            self.default_headers["X-API-Key"] = api_key
        if bearer_token:
            self.default_headers["Authorization"] = f"Bearer {bearer_token}"

        # Add default content type
        if "Content-Type" not in self.default_headers:
            self.default_headers["Content-Type"] = "application/json"

    @asynccontextmanager
    async def _get_client(self):
        """Context manager for httpx.AsyncClient."""
        async with httpx.AsyncClient(
            timeout=self.timeout,
            headers=self.default_headers,
            follow_redirects=True,
        ) as client:
            yield client

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{endpoint}"

    async def get(
        self,
        endpoint: str,
        params: Dict[str, Any] | None = None,
        headers: Dict[str, str] | None = None,
    ) -> Dict[str, Any]:
        """
        Send GET request to the API.

        Args:
            endpoint: API endpoint (e.g., "/users" or "/users/123")
            params: Query parameters
            headers: Additional headers for this request

        Returns:
            JSON response as dictionary

        Raises:
            httpx.HTTPStatusError: If response status is 4xx or 5xx
        """
        async with self._get_client() as client:
            response = await client.get(
                self._build_url(endpoint),
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()

    async def post(
        self,
        endpoint: str,
        data: Dict[str, Any] | None = None,
        json: Dict[str, Any] | None = None,
        headers: Dict[str, str] | None = None,
    ) -> Dict[str, Any]:
        """
        Send POST request to the API.

        Args:
            endpoint: API endpoint
            data: Form data to send
            json: JSON data to send
            headers: Additional headers for this request

        Returns:
            JSON response as dictionary

        Raises:
            httpx.HTTPStatusError: If response status is 4xx or 5xx
        """
        async with self._get_client() as client:
            response = await client.post(
                self._build_url(endpoint),
                data=data,
                json=json,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()

    async def put(
        self,
        endpoint: str,
        json: Dict[str, Any] | None = None,
        headers: Dict[str, str] | None = None,
    ) -> Dict[str, Any]:
        """
        Send PUT request to the API.

        Args:
            endpoint: API endpoint
            json: JSON data to send
            headers: Additional headers for this request

        Returns:
            JSON response as dictionary

        Raises:
            httpx.HTTPStatusError: If response status is 4xx or 5xx
        """
        async with self._get_client() as client:
            response = await client.put(
                self._build_url(endpoint),
                json=json,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()

    async def patch(
        self,
        endpoint: str,
        json: Dict[str, Any] | None = None,
        headers: Dict[str, str] | None = None,
    ) -> Dict[str, Any]:
        """
        Send PATCH request to the API.

        Args:
            endpoint: API endpoint
            json: JSON data to send
            headers: Additional headers for this request

        Returns:
            JSON response as dictionary

        Raises:
            httpx.HTTPStatusError: If response status is 4xx or 5xx
        """
        async with self._get_client() as client:
            response = await client.patch(
                self._build_url(endpoint),
                json=json,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()

    async def delete(
        self,
        endpoint: str,
        headers: Dict[str, str] | None = None,
    ) -> Dict[str, Any] | None:
        """
        Send DELETE request to the API.

        Args:
            endpoint: API endpoint
            headers: Additional headers for this request

        Returns:
            JSON response as dictionary (if response has content), None otherwise

        Raises:
            httpx.HTTPStatusError: If response status is 4xx or 5xx
        """
        async with self._get_client() as client:
            response = await client.delete(
                self._build_url(endpoint),
                headers=headers,
            )
            response.raise_for_status()

            # DELETE may return empty response
            if response.content:
                return response.json()
            return None

    async def request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Send generic HTTP request.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE, etc.)
            endpoint: API endpoint
            **kwargs: Additional arguments passed to httpx.request

        Returns:
            JSON response as dictionary

        Raises:
            httpx.HTTPStatusError: If response status is 4xx or 5xx
        """
        async with self._get_client() as client:
            response = await client.request(
                method=method.upper(), url=self._build_url(endpoint), **kwargs
            )
            response.raise_for_status()

            if response.content:
                return response.json()
            return {}


# Convenience function for quick client creation
def create_client(
    base_url: str, api_key: str | None = None, bearer_token: str | None = None, **kwargs
) -> RestfulAPIClient:
    """
    Create a new RESTful API client instance.

    Args:
        base_url: Base URL of the API
        api_key: Optional API key for authentication
        bearer_token: Optional bearer token for authentication
        **kwargs: Additional arguments passed to RestfulAPIClient

    Returns:
        Configured RestfulAPIClient instance

    Example:
        >>> client = create_client("https://api.example.com", api_key="your-key")
        >>> result = await client.get("/users")
    """
    return RestfulAPIClient(
        base_url=base_url, api_key=api_key, bearer_token=bearer_token, **kwargs
    )


async def get_response(response: httpx.Response) -> Dict[str, Any]:
    """Get response from API.

    Args:
        response (Response): Response from API

    Returns:
        Dict[str, Any]: Response data
    """
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "result": "failed",
            "code": response.status_code,
            "message": response.text,
        }
