from abc import ABC

from aiohttp import web

from app.repository_manager import RepositoryManager


class BaseView(web.View, ABC):
    repo: RepositoryManager

    def __init__(self, *args, repo: RepositoryManager, **kwargs):
        self.repo = repo
        super().__init__(*args, **kwargs)
