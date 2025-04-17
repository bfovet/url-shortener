from beanie import Document
from pydantic import HttpUrl


class Url(Document):

    class Settings:
        name = "urls"

    url: HttpUrl
    id: str
