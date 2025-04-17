from fastapi import APIRouter, HTTPException, status
from pydantic import HttpUrl
from urllib.parse import urlparse

import requests

from url_shortener.models import ShortenedUrl
from url_shortener.db.session import database


router = APIRouter()


def is_url(url: str):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def check_url_is_alive(url: str):
    response = requests.head(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=f"URL {response.reason}")


@router.post(
    "/shorten",
    status_code=status.HTTP_201_CREATED,
    response_model=ShortenedUrl,
    summary="Shorten a URL",
    description="Shorten a URL."
)
async def shorten_url(url: HttpUrl) -> ShortenedUrl:
    check_url_is_alive(str(url))

    session = database
    inserted_url = await session["urls"].insert_one({
        "original_url": str(url),
        "short_link": "XXXXX"
    })

    inserted_url = await session["urls"].find_one({"_id": inserted_url.inserted_id})

    return ShortenedUrl(id=str(inserted_url["_id"]),
                        original_url=inserted_url["original_url"],
                        short_link=inserted_url["short_link"])
