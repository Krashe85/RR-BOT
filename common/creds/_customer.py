from common.helpers.enum import MarketSystemType
from common.helpers.types import MarketType
from common.models.platform.creds import MarketCreds


class AbstractCreds:
    CREDS_MARKET = None

    def __init__(self, creds_db: MarketCreds):
        self._creds: MarketCreds = creds_db

        self._market = MarketType(self._creds.market_type)
        self._market_system = MarketSystemType(self._creds.system_type)

        if self._market != self.CREDS_MARKET:
            raise RuntimeError("Incorrect model market type!")

    @property
    def market_system(self) -> MarketSystemType:
        return self._market_system





