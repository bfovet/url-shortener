"""
URL shortener - a URL shortener service
"""

from beanie import init_beanie
from fastapi import FastAPI

from url_shortener.db.session import client, database
from url_shortener.keygen.counter import RedisKeyCounter
from url_shortener.models import ShortenedUrl
from url_shortener.routes import router


async def lifespan(app: FastAPI):
    # Initialize MongoDB
    pong = await client.admin.command("ping")
    if int(pong["ok"]) != 1:
        raise Exception("Error connecting to database cluster")
    else:
        print("Connected to database cluster")

    # Initialize key generation counter and database
    _ = RedisKeyCounter()

    await init_beanie(database, document_models=[ShortenedUrl])
    app.include_router(router, prefix="/api/v1")

    yield

    client.close()


app = FastAPI(title="URL shortener", lifespan=lifespan)
