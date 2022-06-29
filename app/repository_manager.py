from app.foobar.repository import FooRepo, BarRepo


class RepositoryManager:
    def __init__(self, db):
        self._db = db
        self.foo = FooRepo(self._db)
        self.bar = BarRepo(self._db)
