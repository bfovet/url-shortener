from fastapi import HTTPException
import requests


def check_url_is_alive(url: str):
    response = requests.head(url)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail=f"URL {response.reason}"
        )