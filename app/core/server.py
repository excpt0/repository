import logging

from aiohttp import web

from app import settings

logger = logging.getLogger(__name__)


class Server:
    def __init__(self, db=None, routes=None):
        self.db = db
        self.routes = routes
        self.host = settings.APP_HOST
        self.port = settings.APP_PORT

    def init_app(self):
        app = web.Application()
        app.add_routes(self.routes)
        app.cleanup_ctx.append(self.init_db)
        self.app = app

    async def init_db(self, app):
        if not self.db:
            logger.warning(
                'Cannot init DB connection. '
                'No database host in settings.',
            )
            yield
            return

        app['db'] = self.db
        print('Running DB on %s', settings.DB_DSN)

        await self.db.connect()
        yield
        await self.db.disconnect()

    def run(self):
        self.init_app()
        logger.info('Running app on %s:%s', self.host, self.port)
        web.run_app(self.app, host=self.host, port=self.port)
