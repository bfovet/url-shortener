from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends, status, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl
from redis import asyncio as redis

from url_shortener.keygen.session import get_redis
from url_shortener.models import ShortenedUrl

# from url_shortener.routes import router
from url_shortener.db.session import initialize_db
from url_shortener.shortener import generate_hash_url
from url_shortener.utils import check_url_is_alive


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    app.mongodb_client, app.database = await initialize_db()
#     app.include_router(router, prefix="/api/v1")
    yield
    app.mongodb_client.close()


app = FastAPI(title="URL shortener", lifespan=db_lifespan)


@app.post("/shorten",
          status_code=status.HTTP_201_CREATED,
          summary="Shorten a URL")
async def shorten_url(
    url: HttpUrl, redis_client: Annotated[redis.Redis, Depends(get_redis)]
) -> ShortenedUrl:
    check_url_is_alive(url)
    hash_key = await generate_hash_url(url, redis_client)

    new_url = await ShortenedUrl(original_url=str(url), hash_key=hash_key).create()
    created_url = await ShortenedUrl.get(new_url.id)

    return created_url


@app.get("/{hash_key}",
         status_code=status.HTTP_302_FOUND,
         summary="Redirect")
async def redirect(hash_key: str) -> RedirectResponse:
    url = await app.database["urls"].find_one({"hash_key": hash_key})
    if url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")

    return RedirectResponse(url=url["original_url"])
