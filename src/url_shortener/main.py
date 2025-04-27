from typing import Annotated, Any, AsyncIterator

# from beanie import init_beanie
from fastapi import FastAPI, Depends
from pydantic import HttpUrl
from redis import asyncio as redis

# from url_shortener.db.session import client, database
# from url_shortener.keygen.counter import RedisKeyCounter
from url_shortener.keygen.session import get_redis
from url_shortener.models import ShortenedUrl

# from url_shortener.routes import router
from url_shortener.shortener import generate_hash_url
from url_shortener.utils import check_url_is_alive


# async def lifespan(app: FastAPI):
#     # Initialize MongoDB
#     pong = await client.admin.command("ping")
#     if int(pong["ok"]) != 1:
#         raise Exception("Error connecting to database cluster")
#     else:
#         print("Connected to database cluster")

#     # Initialize key generation counter and database
#     _ = RedisKeyCounter()

#     await init_beanie(database, document_models=[ShortenedUrl])
#     app.include_router(router, prefix="/api/v1")

#     yield

#     client.close()


# app = FastAPI(title="URL shortener", lifespan=lifespan)


app = FastAPI()


@app.post("/shorten")
async def shorten_url(
    url: HttpUrl, redis_client: Annotated[redis.Redis, Depends(get_redis)]
) -> ShortenedUrl:
    check_url_is_alive(url)
    hash_key = await generate_hash_url(url, redis_client)
    return {"id": "0", "original_url": str(url), "hash_key": hash_key}
