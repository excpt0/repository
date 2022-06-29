from app.core.repository import AbstractRepository
from app.foobar.tables import FooTable, BarTable


class FooRepo(AbstractRepository):
    table = FooTable


class BarRepo(AbstractRepository):
    table = BarTable
