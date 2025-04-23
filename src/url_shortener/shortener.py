import base64
import hashlib

import redis
from pydantic import HttpUrl

from url_shortener.keygen.counter import get_next_id


def generate_hash_url_with_id(url: HttpUrl, id: int) -> str:
    hash_object = hashlib.sha512(f"{url}{id}".encode())
    hash_base64 = base64.urlsafe_b64encode(str.encode(hash_object.hexdigest())).decode("utf-8")
    return hash_base64[:7]


async def generate_hash_url(url: HttpUrl, redis_client: redis.Redis) -> str:
    id = await get_next_id(redis_client)
    hash_key = generate_hash_url_with_id(url, id)
    return hash_key
