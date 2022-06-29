from aiohttp import web

from app.core.view import BaseView


class FooView(BaseView):
    async def post(self):
        data = await self.request.json()
        await self.repo.foo.create(
            bar_id=data['bar_id'],
            status=data['status'],
        )

        return web.json_response(data={'success': True})

    async def get(self):
        results = await self.repo.foo.get_list()

        return web.json_response(data={
            'success': True,
            'items': [dict(r) for r in results],
        })


class BarView(BaseView):
    async def post(self):
        data = await self.request.json()
        await self.repo.bar.create(
            name=data['name'],
        )

        return web.json_response(data={'success': True})

    async def get(self):
        results = await self.repo.bar.get_list()

        return web.json_response(data={
            'success': True,
            'items': [dict(r) for r in results],
        })
