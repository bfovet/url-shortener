import base64
import hashlib
from collections import deque

from pydantic import HttpUrl

from url_shortener.keygen.counter import RedisKeyCounter


def get_next_id() -> int:
    counter = RedisKeyCounter()
    counter.get_ids()
    return counter.ids.popleft()


def generate_hash_url(url: HttpUrl, id: int = None) -> str:
    if not id:
        id = get_next_id()
    hash_object = hashlib.sha512(f"{url}{id}".encode())
    hash_base64 = base64.urlsafe_b64encode(str.encode(hash_object.hexdigest())).decode("utf-8")

    return hash_base64[:7]
