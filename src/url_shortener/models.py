# from beanie import Document
from pydantic import BaseModel, HttpUrl


class ShortenedUrl(BaseModel):
    id: str
    original_url: HttpUrl
    hash_key: str
