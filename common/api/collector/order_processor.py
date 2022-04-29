import datetime

from application.common.api.customer.customer import Customer
from application.common.api.collector.product_processor import ProductProcessor
from application.common.database import db
from application.common.models.platform.order import Orders
from application.common.objects.orders import MarketOrder


class OrderProcessor:
    def __init__(self, order: MarketOrder, customer: Customer):
        self._order = order
        self._customer = customer

    def db_synchronize(self):
        exist_order = Orders.query.filter(Orders.market_identity == self._order.market_identification).first()
        if exist_order is not None:
            return

        new_order = Orders(customer=self._customer.id,
                           market_identity=self._order.market_identification,
                           market_type=self._order.marketplace_type.value,
                           creation_date=self._order.market_date,
                           status=self._order.status.value,
                           price=self._order.price,
                           product_count=self._order.product_count)
        new_order.save()

        for product in self._order.products:
            sync_product = ProductProcessor(product, self._customer)
            sync_product.db_synchronize(self._order.market_date.date())

    @classmethod
    def get_order_from_date(cls, customer: Customer, start_date: datetime.datetime, end_date: datetime.datetime):
        orders_list = Orders.query.filter(Orders.creation_date <= end_date,
                                          Orders.creation_date >= start_date,
                                          Orders.customer == customer.id).all()
        result = []
        for order_model in orders_list:
            result.append(MarketOrder.get_from_model(order_model))

        return result
