"""Application configuration."""

from dataclasses import dataclass


@dataclass
class AppConfig:
    """Configuration for the demo application."""

    api_base_url: str = "https://api.example.com"
    timeout_seconds: int = 30
    max_retries: int = 3
    debug: bool = False
