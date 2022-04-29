from common.helpers.enum import Marketplace


class MarketProductStocks:
    def __init__(self, marketplace: Marketplace, sku: str, quantity: int):
        self.marketplace = marketplace
        self.sku = sku
        self.quantity = quantity

    def union(self, other_product):
        self.quantity += other_product.quantity
