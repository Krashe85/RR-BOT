from enum import Enum


class Marketplace(Enum):
    OZON = "OZON"
    YANDEX = "YANDEX"
    WILDBERRIES = "WILDBERRIES"
    ALI_EXPRESS = "ALI_EXPRESS"


class HttpMethod(Enum):
    GET = "get"
    POST = "post"
    PUT = "put"


class MarketSystemType(Enum):
    FBO = "FBO"
    FBS = "FBS"
