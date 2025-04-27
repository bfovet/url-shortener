import httpx
import pytest

from fastapi import status


@pytest.mark.asyncio
async def test_shorten_url(test_client: httpx.AsyncClient) -> None:
    response = await test_client.post(
        "/shorten", params={"url": "https://github.com/bfovet"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["original_url"] == "https://github.com/bfovet"
    assert response.json()["hash_key"] == "ZDc0NGQ"
