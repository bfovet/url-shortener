import redis
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0  # Index of Redis DB used for the counters


redis = redis.Redis(host=Settings().redis_url,
                    port=Settings().redis_port,
                    db=Settings().redis_db)
