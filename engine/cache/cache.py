import datetime

from engine.cache.storage.impl.file import FileCacheStorage
from engine.cache.storage.istorage import ICacheStorage


class Cache:
    def __init__(self, namespace: str, storage=FileCacheStorage):
        self.__namespace = namespace
        self.__storage: ICacheStorage = storage(namespace)
        self.__storage.check_freshness()
        self.__global_lifetime = None

    @property
    def exist(self) -> bool:
        return self.__storage.can_created()

    @property
    def namespace(self):
        return self.__namespace

    def set_global_lifetime(self, timedelta: datetime.timedelta):
        if timedelta is None:
            raise RuntimeError("Time is not null")

        self.__storage.set_freshness(timedelta=timedelta)
        self.__global_lifetime = timedelta

    def get(self, variable, default=None):
        return self.__storage.get(variable=variable, default=default)

    def set(self, variable, value):
        self.__storage.set(variable=variable, value=value)
        if self.__global_lifetime is not None:
            self.set_global_lifetime(self.__global_lifetime)

    def clear(self):
        self.__storage.clear()

    def refresh(self):
        self.__storage.refresh()
