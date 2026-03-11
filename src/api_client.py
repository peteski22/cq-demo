"""HTTP API client with retry logic."""

import time
from datetime import datetime

import httpx

from .config import AppConfig


class APIClient:
    """Client for communicating with the demo API."""

    def __init__(self, config: AppConfig):
        self.config = config
        self.base_url = config.api_base_url
        self.client = httpx.Client(timeout=config.timeout_seconds)

    def get(self, path: str, params: dict = None) -> dict:
        """Make a GET request with retry logic."""
        url = f"{self.base_url}/{path}"
        last_error = None

        for attempt in range(self.config.max_retries):
            try:
                response = self.client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                last_error = e
                if e.response.status_code == 429:
                    time.sleep(2 ** attempt)
                    continue
                raise
            except httpx.TransportError as e:
                last_error = e
                time.sleep(2 ** attempt)

        raise last_error

    def post(self, path: str, data: dict) -> dict:
        """Make a POST request."""
        url = f"{self.base_url}/{path}"
        response = self.client.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def get_items(self, since: str = None) -> list[dict]:
        """Fetch items, optionally filtering by date."""
        params = {}
        if since:
            # Parse and reformat the date to ensure consistent format
            dt = datetime.strptime(since, "%Y-%m-%d")
            params["since"] = dt.strftime("%Y-%m-%dT00:00:00Z")
        return self.get("items", params=params)

    def create_item(self, name: str, tags: list[str] = None) -> dict:
        """Create a new item."""
        payload = {"name": name}
        if tags:
            payload["tags"] = ",".join(tags)
        return self.post("items", payload)

    def close(self):
        """Close the underlying HTTP client."""
        self.client.close()
