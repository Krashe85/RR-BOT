from sqlalchemy import Column, String, Integer, JSON, ForeignKey

from engine.db import BaseModel


class MarketCreds(BaseModel):
    __tablename__ = 'market_creds'

    id = Column(Integer, autoincrement=True, primary_key=True)
    customer = Column(Integer, ForeignKey('customer.id'), nullable=False)
    system_type = Column(String(10))
    market_type = Column(String(50))
    payload = Column(JSON)

    @classmethod
    def get_from_customer_and_marketplace(cls, customer_id: int, marketplace: str):
        return cls.query.filter(cls.customer == customer_id, cls.market_type == marketplace).first()
