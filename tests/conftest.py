from typing import AsyncIterator
from unittest import mock

import fakeredis
import httpx
import pytest_asyncio
from redis import asyncio as redis

from url_shortener.main import app
from url_shortener.keygen.session import get_redis


@pytest_asyncio.fixture
async def redis_client() -> AsyncIterator[redis.Redis]:
    async with fakeredis.FakeAsyncRedis() as client:
        yield client


@pytest_asyncio.fixture
async def app_client(redis_client: redis.Redis) -> AsyncIterator[httpx.AsyncClient]:
    async def get_redis_override() -> redis.Redis:
        return redis_client

    transport = httpx.ASGITransport(app=app)  # type: ignore[arg-type] # https://github.com/encode/httpx/issues/3111
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as app_client:
        with mock.patch.dict(app.dependency_overrides, {get_redis: get_redis_override}):
            yield app_client