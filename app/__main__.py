import uvloop
from databases import Database

from app import settings
from app.core.server import Server
from app.routes import make_routes


def main() -> None:
    uvloop.install()
    db = Database(url=settings.DB_DSN)
    Server(
        routes=make_routes(db),
        db=db,
    ).run()


if __name__ == "__main__":
    main()
