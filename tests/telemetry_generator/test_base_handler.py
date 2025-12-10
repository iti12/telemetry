import asyncio
import pytest
from aiohttp import web

from telemetry_generator.handlers.base import BaseHandler


class DummyHandler(BaseHandler):
    def __init__(self):
        super().__init__("DummyHandler")

    async def handle(self, request):
        await asyncio.sleep(0.01)
        return web.Response(text="ok")


@pytest.mark.asyncio
async def test_base_handler_tracks_latency(aiohttp_client):
    handler = DummyHandler()
    app = web.Application()
    app.router.add_get("/test", handler)

    client = await aiohttp_client(app)
    resp = await client.get("/test")

    assert resp.status == 200
    assert await resp.text() == "ok"
    assert handler.request_count == 1
    assert handler.avg_latency > 0
