import base64
import hashlib
from collections import deque

from pydantic import HttpUrl

from url_shortener.keygen.counter import RedisKeyCounter


def generate_hash_url(url: HttpUrl) -> str:
    counter = RedisKeyCounter()
    counter.get_ids()
    next_id = counter.ids.popleft()
    hash_object = hashlib.sha512(f"{url}{next_id}".encode())
    hash_base64 = base64.urlsafe_b64encode(str.encode(hash_object.hexdigest())).decode("utf-8")

    return hash_base64[:7]
