from collections import deque

from url_shortener.keygen.session import redis


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisKeyCounter(metaclass=Singleton):
    counter_key = "url_counter"
    incr_value = 1000
    ids: deque = deque()

    def get_ids(self):
        # print(f"ids={self.ids} ({len(self.ids)} left)")
        if not self.ids:
            print(f"Requesting {self.incr_value} values from key generation service")
            self.ids = self._get_ids()

    def _get_ids(self):
        pipe = redis.pipeline()
        pipe.setnx(self.counter_key, 0)
        pipe.get(self.counter_key)
        pipe.incrby(self.counter_key, self.incr_value)
        res = pipe.execute()

        return deque(range(int(res[1]), res[-1]))
