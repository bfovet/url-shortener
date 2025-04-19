from beanie import Document
from pydantic import HttpUrl


class ShortenedUrl(Document):

    class Settings:
        name = "urls"

    id: str
    original_url: HttpUrl
    hash_key: str
