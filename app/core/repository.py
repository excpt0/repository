from abc import ABC
from typing import List

from databases.backends.postgres import Record
from sqlalchemy import select, update, insert


class AbstractRepository(ABC):
    table = None

    allowed_filter_fields = {}

    def __init__(self, db):
        self._db = db

    def _build_filtering(self, filter_fields, table) -> list:
        parts = []
        for field_name, op in self.allowed_filter_fields.items():
            val = filter_fields.get(field_name)

            if val is None:
                continue

            if isinstance(op, str):
                field = getattr(table, field_name)
                parts.append(getattr(field, op)(val))
            elif callable(op):
                parts.append(op(val))
            else:
                TypeError(
                    'Operator must be instance of `str` or `callable`'
                )

        return parts

    async def get(self, **filters) -> Record:
        return await self._db.fetch_one(
            query=select(self.table).where(
                *self._build_filtering(filters, self.table),
            ),
        )

    async def get_list(self, **filters) -> List[Record]:
        return await self._db.fetch_all(
            query=select(self.table).where(
                *self._build_filtering(filters, self.table),
            ),
        )

    async def update(self, _id, **fields) -> Record:
        await self._db.execute(
            update(self.table).where(self.table.id == _id),
            values=fields,
        )

        return await self.get(id=_id)

    async def create(self, **fields) -> Record:
        record_id = await self._db.execute(
            insert(self.table).returning(self.table.id),
            values=fields,
        )

        return await self.get(id=record_id)
