from aiohttp import web
from dependency_injector import providers

from app.foobar.urls import urls
from app.repository_manager import RepositoryManager


class ClassBasedView(providers.Factory):

    def as_view(self):
        async def _view(request, *args, **kwargs):
            return await self.__call__(request, *args, **kwargs)

        return _view


def make_routes(db):
    repo = RepositoryManager(db)
    url_batches = [
        urls,
    ]

    app_routes = []

    for batch in url_batches:
        for path, handler in batch:
            app_routes.append(web.view(
                path,
                ClassBasedView(handler, repo=repo).as_view()
            ))

    return app_routes
