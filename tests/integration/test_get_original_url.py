import httpx
import pytest

from fastapi import status


@pytest.mark.asyncio
async def test_get_original_url(test_client: httpx.AsyncClient) -> None:
    input_url = "https://github.com/bfovet"
    r = await test_client.post("/shorten", params={"url": input_url})
    response = await test_client.get("/ZDc0NGQ")
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
