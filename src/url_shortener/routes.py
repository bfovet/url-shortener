from fastapi import APIRouter, status

from url_shortener.models import Url


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Url
)
async def create_url(url: Url) -> Url:
    return Url(url="https://foo.bar", id="1")
