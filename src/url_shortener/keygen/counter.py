from collections import deque

from redis import asyncio as redis


class IdsProvider:
    def __init__(self):
        self._counter_key = "url_counter"
        self._incr_value = 1000
        self._ids: deque = deque()

    async def get_ids(self, redis_client: redis.Redis) -> deque:
        if not self._ids:
            print(f"Requesting {self._incr_value} values from key generation service")
            self._ids = await self._get_ids(redis_client)

        return self._ids

    async def _get_ids(self, redis_client: redis.Redis) -> deque:
        pipe = redis_client.pipeline()
        pipe.setnx(self._counter_key, 0)
        pipe.get(self._counter_key)
        pipe.incrby(self._counter_key, self._incr_value)
        res = await pipe.execute()

        return deque(range(int(res[1]), res[-1]))


ids_provider = IdsProvider()


async def get_next_id(redis_client: redis.Redis):
    next_ids = await ids_provider.get_ids(redis_client)
    return next_ids.popleft()
