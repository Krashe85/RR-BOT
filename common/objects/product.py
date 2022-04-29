from common.helpers.enum import Marketplace


class MarketSalesObj:
    def __init__(self, month_number: int, ozon_sales: int, wb_sales: int, yandex_sales: int, aliexpress_sales: int):
        self.month_number = month_number
        self.ozon_sales = ozon_sales
        self.wb_sales = wb_sales
        self.yandex_sales = yandex_sales
        self.aliexpress_sales = aliexpress_sales

    @classmethod
    def get_from_model(cls, model, month_number):
        return cls(month_number=month_number,
                   ozon_sales=model.ozon_sales,
                   wb_sales=model.wb_sales,
                   yandex_sales=model.yandex_sales,
                   aliexpress_sales=model.aliexpress_sales)


class MarketProduct:
    def __init__(self, sku: str, title: str, price: float, marketplace: Marketplace = None):
        self.sku: str = sku
        self.title: str = title
        self.price: float = float(price)
        self.marketplace: Marketplace | None = marketplace
        self._stock_pool: dict[Marketplace, int] = dict()

        self._sales_info: MarketSalesObj | None = None

        self._find_infomation = {
            Marketplace.OZON: False,
            Marketplace.YANDEX: False,
            Marketplace.WILDBERRIES: False,
            Marketplace.ALI_EXPRESS: False
        }

    @property
    def sales(self) -> MarketSalesObj:
        return self._sales_info

    def add_sales_obj(self, obj: MarketSalesObj):
        self._sales_info = obj

    def check_find(self, marketplace: Marketplace) -> bool:
        return self._find_infomation.get(marketplace, False)

    def set_find(self, marketplace: Marketplace) -> None:
        self._find_infomation[marketplace] = True

    def add_stock(self, marketplace: Marketplace, count: int):
        self._stock_pool[marketplace] = count

    def get_stock(self, marketplace: Marketplace) -> int:
        return self._stock_pool.get(marketplace, 0)

    @classmethod
    def get_from_model(cls, model):
        result = cls(sku=model.sku,
                     title=model.title,
                     price=model.price)

        if model.ozon_find is True:
            result.set_find(Marketplace.OZON)
            result.add_stock(Marketplace.OZON, model.ozon_stocks)

        if model.wb_find is True:
            result.set_find(Marketplace.WILDBERRIES)
            result.add_stock(Marketplace.WILDBERRIES, model.wb_stocks)

        if model.yandex_find is True:
            result.set_find(Marketplace.YANDEX)
            result.add_stock(Marketplace.YANDEX, model.yandex_stocks)

        if model.aliexpress_find is True:
            result.set_find(Marketplace.ALI_EXPRESS)
            result.add_stock(Marketplace.ALI_EXPRESS, model.aliexpress_stocks)

        return result
