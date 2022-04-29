import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from ._query import RetryingQuery

engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PWD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_BASE')}"
    , pool_size=100, pool_pre_ping=True, pool_recycle=1800, pool_timeout=1800)

# Session = sessionmaker(bind=engine, query_cls=RetryingQuery)

metadata = MetaData()
session_factory = sessionmaker(bind=engine, query_cls=RetryingQuery, autocommit=False, autoflush=True)
db = scoped_session(session_factory)


class SqlBase(object):
    query_class = RetryingQuery

    def save(self):
        db.add(self)
        self._flush()
        return self

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            getattr(self, attr)
            setattr(self, attr, value)
        return self.save()

    def delete(self):
        db.delete(self)
        self._flush()

    @staticmethod
    def _flush():
        try:
            db.flush()
        except DatabaseError:
            db.rollback()
            raise


BaseModel = declarative_base(cls=SqlBase)

BaseModel.query = db.query_property(query_cls=RetryingQuery)
BaseModel.query_function = db.query
BaseModel.execute = db.execute
