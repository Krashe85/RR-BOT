import datetime

from application.common.helpers.status import OrderStatus
from application.helpers.enums import Marketplace
from application.common.objects.product import MarketProduct


class MarketOrder:
    def __init__(self, marketplace: Marketplace, status: OrderStatus,
                 market_identification: str, market_date: datetime.datetime,
                 market_amount: float = 0, product_count: int = 0):

        self.marketplace_type = marketplace
        self.market_identification = market_identification
        self.market_amount = int(market_amount)
        self.market_date = market_date
        self._products: list[MarketProduct] = []
        self.status = status
        self.product_count = product_count

    def add_product(self, product: MarketProduct, my_price: float = None):
        if my_price:
            self.market_amount += my_price
        else:
            self.market_amount += float(product.price)

        self._products.append(product)

    @property
    def products(self):
        return self._products

    @property
    def price(self):
        total = 0
        for product in self._products:
            total += product.price
        return total

    def union(self, market_order):
        if market_order.market_date > self.market_date:
            self.market_date = market_order.market_date

        for product in market_order.products:
            self.add_product(product)

    @classmethod
    def get_from_model(cls, model):
        return cls(marketplace=Marketplace(model.market_type),
                   status=OrderStatus(model.status),
                   market_identification=model.market_identity,
                   market_date=model.creation_date,
                   market_amount=model.price)


