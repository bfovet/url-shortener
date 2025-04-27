from typing import Optional

from beanie import Document, PydanticObjectId
from fastapi import HTTPException
from pydantic import Field, HttpUrl


class ShortenedUrl(Document):
    # Use a string for _id, instead of ObjectID
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PydanticObjectId] = Field(alias="_id", default=None, description="MongoDB document ObjectID")
    original_url: HttpUrl
    hash_key: str

    class Settings:
        # Name of the collection to store these URLs.
        name = "urls"


async def get_url(url_id: PydanticObjectId) -> ShortenedUrl:
    url = await ShortenedUrl.get(url_id)
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return url
