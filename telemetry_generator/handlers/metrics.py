from datetime import datetime
from aiohttp import web
from telemetry_generator.handlers.base import BaseHandler


class MetricsHandler(BaseHandler):
    def __init__(self):
        super().__init__("Metrics")

    async def handle(self, request):
        return web.json_response({
            "switches": len(request.app["telemetry"]),
            "timestamp": datetime.utcnow().isoformat(),
        })
