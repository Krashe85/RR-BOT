from sqlalchemy import Column, Integer, String

from engine.db import BaseModel


class CustomerModel(BaseModel):
    __tablename__ = 'customer'

    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    title = Column(String, nullable=True, default=True)

    @classmethod
    def get_from_id(cls, identification: int):
        find = cls.query.filter(cls.id == identification).first()
        if find is None:
            raise RuntimeError("Unknown client")
        return find

    @classmethod
    def get_from_title(cls, title: str):
        find = cls.query.filter(cls.title == title).first()
        if find is None:
            raise RuntimeError("Unknown client")
        return find
