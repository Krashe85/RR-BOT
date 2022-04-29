from common.creds._customer import AbstractCreds
from common.helpers.creds_checker import response_checker
from common.helpers.types import MarketType


class WildberriesApiCreds(AbstractCreds):
    CREDS_MARKET = MarketType.WILDBERRIES

    @property
    @response_checker
    def api_key(self):
        return self._creds.payload.get("api_key", None)