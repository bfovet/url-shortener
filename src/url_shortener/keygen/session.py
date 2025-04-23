from typing import Annotated, Any, AsyncIterator

from pydantic_settings import BaseSettings
from redis import asyncio as redis
from fastapi import Depends, FastAPI


class Settings(BaseSettings):
    redis_url: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0  # Index of Redis DB used for the counters


async def get_redis() -> AsyncIterator[redis.Redis]:
    async with redis.from_url(f"redis://{Settings().redis_url}:{Settings().redis_port}") as client:
        yield client
