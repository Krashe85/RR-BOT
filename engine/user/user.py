from telegram import User, Update

from common.api.customer.customer import Customer
from common.models.customer import CustomerModel
from engine.cache import Cache
from engine.user.permissions import Permissions, PermissionsGroups

_BASE_KEY_USER_GROUP = "permission_group"
_BASE_MARKET_CLIENT = "market_client_id"


def _update_user_pool(new_user):
    cache = Cache("user_pool")
    current_pool = cache.get("pool", list())
    current_pool.append(new_user.telegram)
    cache.set("pool", current_pool)


def _get_current_pool() -> list[int]:
    cache = Cache("user_pool")
    return cache.get("pool", list())


class BotUser:
    def __init__(self, telegram_id: int):
        self._telegram = telegram_id

        self._storage = Cache(f"user_{self._telegram}")
        if self._storage.exist is False:
            self._storage.set(_BASE_KEY_USER_GROUP, "UNKNOWN")
            _update_user_pool(self)

    @property
    def telegram(self) -> int:
        return self._telegram

    @property
    def permissions(self) -> Permissions:
        group_namer = self._storage.get(_BASE_KEY_USER_GROUP, "UNKNOWN")
        return PermissionsGroups.get_from_technical_name(group_namer).value

    @permissions.setter
    def permissions(self, value: str):
        self._storage.get(_BASE_KEY_USER_GROUP, value)

    @property
    def market_customer(self):
        client_id = self._storage.get(_BASE_MARKET_CLIENT, None)
        if client_id is None:
            raise RuntimeError("Client is none!")

        return Customer(CustomerModel.get_from_id(client_id))

    @market_customer.setter
    def market_customer(self, client: Customer):
        self._storage.set(_BASE_MARKET_CLIENT, client.id)

    @classmethod
    def get_all(cls) -> list:
        pool = _get_current_pool()
        result = []

        for telegram in pool:
            result.append(cls(telegram))
        return result


