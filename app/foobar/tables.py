from sqlalchemy import ForeignKey, VARCHAR, Column, Integer
from sqlalchemy.orm import declarative_base

BaseTable = declarative_base()


class BarTable(BaseTable):
    __tablename__ = 'bar'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(128))


class FooTable(BaseTable):
    __tablename__ = 'foo'

    id = Column(Integer, primary_key=True)
    bar_id = Column(Integer, ForeignKey('bar.id'))
    status = Column(VARCHAR(128))
