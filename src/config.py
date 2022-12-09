from dataclasses import dataclass
from multiprocessing import cpu_count

from environs import Env

env = Env()


@dataclass(frozen=True)
class GunicornConfig:
    """Gunicorn configuration."""

    count_workers: int = env.int("WORKERS", cpu_count() * 2 + 1)
    port: int = env.int("PORT", 80)


@dataclass(frozen=True)
class Config:
    """Configuration for the application."""

    cache_max_size: int = env.int("CACHE_MAX_SIZE", 1024)
    cache_ttl: int = env.int("CACHE_TTL", 600)
    debug: bool = env.bool("DEBUG", False)


config = Config()
gunicorn_config = GunicornConfig()

__all__ = ["config", "gunicorn_config"]
