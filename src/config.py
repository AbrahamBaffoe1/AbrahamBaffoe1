"""Configuration management for the agentic code reviewer."""

import os
import logging
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Application configuration."""

    # API Configuration
    anthropic_api_key: str
    anthropic_model: str = "claude-3-5-sonnet-20241022"

    # GitHub Configuration (optional)
    github_token: Optional[str] = None
    github_webhook_secret: Optional[str] = None

    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Web Configuration
    web_host: str = "0.0.0.0"
    web_port: int = 5000
    web_debug: bool = False

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable not set. "
                "See .env.example for setup instructions."
            )

        return cls(
            anthropic_api_key=api_key,
            anthropic_model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
            github_token=os.getenv("GITHUB_TOKEN"),
            github_webhook_secret=os.getenv("GITHUB_WEBHOOK_SECRET"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            web_host=os.getenv("WEB_HOST", "0.0.0.0"),
            web_port=int(os.getenv("WEB_PORT", "5000")),
            web_debug=os.getenv("FLASK_ENV") == "development",
        )


def setup_logging(config: Config) -> None:
    """Setup logging based on configuration."""
    logging.basicConfig(
        level=getattr(logging, config.log_level.upper()),
        format=config.log_format,
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config.from_env()
        setup_logging(_config)
    return _config
