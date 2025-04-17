"""
URL shortener - a URL shortener service
"""

from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings

from url_shortener.models import Url
from url_shortener.routes import router


async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(Settings().mongodb_url)
    pong = await client.admin.command("ping")
    if int(pong["ok"]) != 1:
        raise Exception("Error connecting to database cluster")
    else:
        print("Connected to database cluster")

    await init_beanie(client.get_default_database(), document_models=[Url])
    app.include_router(router, prefix="/api/v1")

    yield

    client.close()


app = FastAPI(title="URL shortener", root_path="/api/v1", lifespan=lifespan)


class Settings(BaseSettings):
    mongodb_url: str = "mongodb://127.0.0.1:27017/urls"
