from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_url: str = "mongodb://127.0.0.1:27017/urls"


client = AsyncIOMotorClient(Settings().mongodb_url)
database = client.shortener
