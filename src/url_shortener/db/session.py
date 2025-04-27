from pydantic_settings import BaseSettings
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from url_shortener.models import ShortenedUrl


class Settings(BaseSettings):
    mongodb_url: str = "mongodb://127.0.0.1:27017/urls"


async def initialize_db():
    mongodb_client = AsyncIOMotorClient(Settings().mongodb_url)
    database = mongodb_client.get_default_database()
    await init_beanie(database, document_models=[ShortenedUrl])

    return mongodb_client, database
