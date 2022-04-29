from common.creds._customer import AbstractCreds
from common.helpers.creds_checker import response_checker
from common.helpers.types import MarketType


class YandexApiCreds(AbstractCreds):
    CREDS_MARKET = MarketType.YANDEX

    @property
    @response_checker
    def token(self):
        return self._creds.payload.get("token", None)

    @property
    @response_checker
    def oauth_client(self):
        return self._creds.payload.get("oauth_client", None)

    @property
    @response_checker
    def client_id(self):
        return self._creds.payload.get("client_id", None)

