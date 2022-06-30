# Repository examples

## Common Repository implementation 

```python
class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError
    
    
class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference):
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(model.Batch).all()

```

## Table based Repository implementation

```python
class AbstractRepository(abc.ABC):
    table = None

    allowed_filter_fields = {}

    def __init__(self, conn):
        self._conn = conn

    def _build_filtering(self, filter_fields) -> list:
        parts = []
        for field_name, op in self.allowed_filter_fields.items():
            val = filter_fields.get(field_name)

            if val is None:
                continue

            field = getattr(self.table, field_name)
            parts.append(getattr(field, op)(val))
   
        return parts

    async def get(self, **filters) -> Record:
        return await self._conn.fetch_one(
            query=select(self.table).where(
                *self._build_filtering(filters),
            ),
        )

    async def update(self, _id, **fields) -> Record:
        await self._conn.execute(
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

    async def list(self, **filters) -> List[Record]:
        return await self._db.fetch_all(
            query=select(self.table).where(
                *self._build_filtering(filters),
            )
        )

        
class FooBarRepository(AbstractRepository):
    table = FooBarTable
    allowed_filter_fields = {
        'id': '__eq__',
        'name': '__eq__',
    }

```

## Transformer Repository

```python

@dataclass
class FooEntity:
    name: str
    bar: int
    
    def to_model(self):
        return FooModel(
            name=self.name,
            bar=self.bar,
        )
    
    @classmethod
    def from_model(cls, model):
        return cls(
            name=model.name,
            bar=model.bar,
        )

class AbstractTransformerRepository(abc.ABC):
    entity = None
    model = None
    
    @abc.abstractmethod
    def add(self, entity):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference):
        raise NotImplementedError

    
class FooRepository(AbstractTransformerRepository):
    entity = FooEntity
    model = FooModel
    
    def __init__(self, session):
        self.session = session

    def add(self, entity):
        self.session.add(entity.to_model())

    def get(self, reference):
        return self.entity.from_model(
            self.session.query(self.model).filter_by(reference=reference).one()
        )

    def list(self):
        results = self.session.query(self.model).all()
        return [self.entity.from_model(r) for r in results]

```
