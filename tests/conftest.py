from typing import AsyncIterator
from unittest import mock

from beanie import init_beanie
from asgi_lifespan import LifespanManager
from mongomock_motor import AsyncMongoMockClient
import fakeredis
import httpx
import pytest_asyncio
from redis import asyncio as redis

from url_shortener.models import ShortenedUrl
from url_shortener.main import app
from url_shortener.keygen.session import get_redis
from url_shortener.db.session import initialize_db


async def mock_database():
    client = AsyncMongoMockClient()
    database = client.get_database("test")
    await init_beanie(database=database,
                      document_models=[ShortenedUrl])

    return client, database


@pytest_asyncio.fixture
async def redis_client() -> AsyncIterator[redis.Redis]:
    async with fakeredis.FakeAsyncRedis() as client:
        yield client


@pytest_asyncio.fixture
async def test_client(redis_client: redis.Redis) -> AsyncIterator[httpx.AsyncClient]:
    async def get_redis_override() -> redis.Redis:
        return redis_client

    # TODO: mocking MongoDB does not work
    async with LifespanManager(app):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test", follow_redirects=False) as ac:
            # with (mock.patch.dict(app.dependency_overrides, {get_redis: get_redis_override}),
            #       mock.patch.dict(app.dependency_overrides, {initialize_db: mock_database})):
            with mock.patch.dict(app.dependency_overrides, {get_redis: get_redis_override}):
                yield ac
