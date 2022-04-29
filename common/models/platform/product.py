from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Float

from engine.db import BaseModel


class Products(BaseModel):
    __tablename__ = 'products'

    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)

    sku = Column(String(50))
    customer = Column(Integer, ForeignKey('customer.id'), nullable=False)
    price = Column(Float, default=0.0)
    title = Column(String(50))

    ozon_find = Column(Boolean, default=False)
    ozon_stocks = Column(Integer, default=-1)

    wb_find = Column(Boolean, default=False)
    wb_stocks = Column(Integer, default=-1)

    yandex_find = Column(Boolean, default=False)
    yandex_stocks = Column(Integer, default=-1)

    aliexpress_find = Column(Boolean, default=False)
    aliexpress_stocks = Column(Integer, default=-1)


class ProductsSales(BaseModel):
    __tablename__ = 'products_sales'

    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)

    year_number = Column(Integer, nullable=False)
    month_number = Column(Integer, nullable=False)
    day_number = Column(Integer, nullable=False)

    ozon_sales = Column(Integer, default=0)
    wb_sales = Column(Integer, default=0)
    yandex_sales = Column(Integer, default=0)
    aliexpress_sales = Column(Integer, default=0)
