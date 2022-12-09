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


@dataclass(frozen=True)
class RedisConfig:
    """Configuration for Redis."""

    use = env.bool("REDIS_USE", False)
    host: str = env.str("REDIS_HOST", "localhost")
    pool_size: int = env.int("REDIS_POOL_SIZE", 10)
    port: int = env.int("REDIS_PORT", 6379)
    db: int = env.int("REDIS_DB", 0)
    password: str = env.str("REDIS_PASSWORD", None)
    url: str = env.str("REDIS_URL", None)

    def get_url(self) -> str:
        """Get Redis URL."""
        if self.url:
            return self.url
        return f"redis://{self.host}:{self.port}/{self.db}"


config = Config()
gunicorn_config = GunicornConfig()
redis_config = RedisConfig()

__all__ = ["config", "gunicorn_config", "redis_config"]
