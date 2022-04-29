from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, Float, ForeignKey

from engine.db import BaseModel


class Orders(BaseModel):
    __tablename__ = 'orders'

    id = Column(Integer, autoincrement=True, primary_key=True)
    customer = Column(Integer, ForeignKey('customer.id'), nullable=False)
    market_type = Column(String(20))

    # Идентивикатор в системе маркетплейса
    market_identity = Column(String(30))
    creation_date = Column(DateTime, default=datetime.now())
    status = Column(String(50))
    price = Column(Float)
    product_count = Column(Integer)

