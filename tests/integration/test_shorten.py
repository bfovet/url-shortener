import httpx
import pytest


@pytest.mark.asyncio
async def test_shorten_url(app_client: httpx.AsyncClient) -> None:
    response = await app_client.post("/shorten", params={"url": "https://github.com/bfovet"})
    assert response.status_code == 200
    assert response.json() == {"id": "0", "original_url": "https://github.com/bfovet", "hash_key": "ZDc0NGQ"}
