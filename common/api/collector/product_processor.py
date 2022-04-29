import datetime
import itertools

from common.api.customer.customer import Customer
from common.helpers.date import generate_range_dates
from common.helpers.enum import Marketplace
from common.models.platform.product import Products, ProductsSales
from common.objects.new_product import MarketProductStocks
from common.objects.product import MarketProduct, MarketSalesObj
from engine.db import db


class ProductDayUnit:
    def __init__(self, date: datetime.date):
        self.date = date
        self._products: list[MarketProduct] = []

    def add_product(self, product: MarketProduct):
        self._products.append(product)

    def add_products(self, products: list[MarketProduct]):
        self._products = list(itertools.chain(self._products, products))

    @property
    def product(self) -> list[MarketProduct]:
        return self._products


class ProductSalesProcessor:
    def __init__(self, product_model: Products, customer: Customer):
        self._product_model = product_model
        self._customer = customer

    def _get_model_from_date(self, date: datetime.date) -> ProductsSales:
        current_month = db.query(ProductsSales).filter(ProductsSales.product_id == self._product_model.id,
                                                       ProductsSales.month_number == date.month,
                                                       ProductsSales.year_number == date.year,
                                                       ProductsSales.day_number == date.day).first()

        if current_month is None:
            current_month = ProductsSales(product_id=self._product_model.id,
                                          month_number=date.month,
                                          year_number=date.year,
                                          day_number=date.day)
            current_month.save()
        return current_month

    def db_synchronize(self, marketplace: Marketplace, date: datetime.date):
        current_month: ProductsSales = self._get_model_from_date(date)

        if marketplace == Marketplace.OZON:
            current_month.ozon_sales += 1
        elif marketplace == Marketplace.YANDEX:
            current_month.yandex_sales += 1
        elif marketplace == Marketplace.WILDBERRIES:
            current_month.wb_sales += 1
        elif marketplace == Marketplace.ALI_EXPRESS:
            current_month.aliexpress_sales += 1
        db.commit()

    @classmethod
    def get_product_sales_from_month_number(cls, customer: Customer,
                                            product: Products,
                                            date: datetime.date) -> ProductsSales:
        sales = cls(product, customer)
        return sales._get_model_from_date(date)


class ProductProcessor:
    def __init__(self, product: MarketProduct, customer: Customer):
        self._product = product
        self._customer = customer

    def db_synchronize(self, date: datetime.date):
        db_product: Products = db.query(Products).filter(Products.sku == self._product.sku,
                                                         Products.customer == self._customer.id).first()
        if db_product is None:
            db_product = Products(customer=self._customer.id,
                                  sku=self._product.sku,
                                  title=self._product.title,
                                  price=self._product.price)
            db_product.save()

        if self._product.marketplace == Marketplace.OZON:
            if db_product.ozon_find is False:
                db_product.ozon_find = True
                db.commit()
        elif self._product.marketplace == Marketplace.YANDEX:
            if db_product.yandex_find is False:
                db_product.yandex_find = True
                db.commit()
        elif self._product.marketplace == Marketplace.WILDBERRIES:
            if db_product.wb_find is False:
                db_product.wb_find = True
                db.commit()

        sales = ProductSalesProcessor(db_product, self._customer)
        sales.db_synchronize(self._product.marketplace, date)

    @staticmethod
    def get_products_from_date(customer: Customer, date: datetime.date) -> list[MarketProduct]:
        products = Products.query.filter(Products.customer == customer.id).all()
        result = []

        for product in products:
            market_product = MarketProduct.get_from_model(product)

            sales = ProductSalesProcessor.get_product_sales_from_month_number(
                customer=customer, product=product, date=date
            )
            market_product.add_sales_obj(MarketSalesObj.get_from_model(sales, date))

            result.append(market_product)
        return result

    @classmethod
    def get_from_dates_unit(cls, customer: Customer, start_date: datetime.date, end_date: datetime.date):
        date_range = generate_range_dates(start_date, end_date)
        result: list[ProductDayUnit] = []

        for current_date in date_range:
            unit = ProductDayUnit(current_date)
            unit.add_products(ProductProcessor.get_products_from_date(customer, current_date))
            result.append(unit)
        result.sort(key=lambda x: x.date, reverse=True)
        return result

    @staticmethod
    def get_product_from_marketplace(customer: Customer, marketplace: Marketplace) -> list[MarketProduct]:
        args = []
        if marketplace == Marketplace.OZON:
            args.append(Products.ozon_find == True)
        elif marketplace == Marketplace.YANDEX:
            args.append(Products.yandex_find == True)
        elif marketplace == Marketplace.WILDBERRIES:
            args.append(Products.wb_find == True)
        elif marketplace == Marketplace.ALI_EXPRESS:
            args.append(Products.aliexpress_find == True)

        finds = Products.query.filter(Products.customer == customer.id, *args).all()

        result: list[MarketProduct] = list()

        for find in finds:
            result.append(MarketProduct.get_from_model(find))
        return result


class ProductStocksProcessor:
    def __init__(self, customer: Customer):
        self._customer = customer

    def fetching_stocks(self, stock_pool: list[MarketProductStocks]):
        for product in stock_pool:
            base_order: Products = Products.query.filter(Products.sku == product.sku,
                                                         Products.customer == self._customer.id).first()
            if base_order is None:
                print("This unknown order!")

            if product.marketplace == Marketplace.OZON:
                base_order.ozon_stocks = product.quantity
            elif product.marketplace == Marketplace.YANDEX:
                base_order.yandex_stocks = product.quantity
            elif product.marketplace == Marketplace.WILDBERRIES:
                base_order.wb_stocks = product.quantity
            elif product.marketplace == Marketplace.ALI_EXPRESS:
                base_order.aliexpress_stocks = product.quantity
            else:
                raise RuntimeError("Unknown marketplace")
            db.commit()
