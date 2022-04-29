from common.creds.ozon import OzonApiCreds
from common.creds.wildberries import WildberriesApiCreds
from common.creds.yandex import YandexApiCreds
from common.models.customer import CustomerModel
from common.models.platform.creds import MarketCreds
from engine.db import db


class Customer:
    def __init__(self, customer_model):
        self._model: CustomerModel = customer_model

    @property
    def id(self):
        return self._model.id

    @property
    def username(self):
        return self._model.title

    def get_ozon_creds(self) -> OzonApiCreds | None:
        creds = MarketCreds.get_from_customer_and_marketplace(self.id, "OZON")
        if creds is None:
            return None
        return OzonApiCreds(creds)

    def get_wb_creds(self) -> WildberriesApiCreds | None:
        creds = MarketCreds.get_from_customer_and_marketplace(self.id, "WILDBERRIES")
        if creds is None:
            return None
        return WildberriesApiCreds(creds)

    def get_yandex_creds(self) -> YandexApiCreds | None:
        creds = MarketCreds.get_from_customer_and_marketplace(self.id, "YANDEX")
        if creds is None:
            return None
        return YandexApiCreds(creds)

    @staticmethod
    def get_all_customer():
        all_customers = db.query(CustomerModel).all()
        result = []

        for customer_model in all_customers:
            result.append(Customer(customer_model))
        return result
