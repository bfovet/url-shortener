from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl

import requests

from url_shortener.models import ShortenedUrl
from url_shortener.db.session import database
from url_shortener.shortener import generate_hash_url


router = APIRouter()


def check_url_is_alive(url: str):
    response = requests.head(url)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail=f"URL {response.reason}"
        )


@router.post(
    "/shorten",
    status_code=status.HTTP_201_CREATED,
    response_model=ShortenedUrl,
    summary="Shorten a URL",
    description="Shorten a URL.",
)
async def shorten_url(url: HttpUrl) -> ShortenedUrl:
    check_url_is_alive(str(url))

    session = database
    inserted_url = await session["urls"].insert_one(
        {"original_url": str(url), "hash_key": generate_hash_url(url)}
    )

    inserted_url = await session["urls"].find_one({"_id": inserted_url.inserted_id})

    return ShortenedUrl(
        id=str(inserted_url["_id"]),
        original_url=inserted_url["original_url"],
        hash_key=inserted_url["hash_key"],
    )


@router.get(
    "/{hash_key}",
    status_code=status.HTTP_302_FOUND,
    response_model=None,
    summary="Redirect",
)
async def redirect(hash_key: str) -> RedirectResponse:
    session = database
    url = await session["urls"].find_one({"hash_key": hash_key})

    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL not found"
        )

    return RedirectResponse(url=url["original_url"])
