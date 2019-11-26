import redis
from dynaconf import settings


class RedisSrv:
    def __init__(self):
        self.redis = redis.Redis(host=settings.REDIS_HOST,
                                 port=settings.REDIS_PORT,
                                 db=settings.REDIS_DB_ID,
                                 decode_responses=True)
        self.watchers = list()

    def add_watcher(self, watcher):
        self.watchers.append(watcher)

    def hgetall(self, name):
        return self.redis.hgetall(name)

    def hset(self, name, key, value):
        res = self.redis.hset(name, key, value)
        for watcher in self.watchers:
            watcher.invoke(name=name, key=key, value=value)
        return res