from aiohttp import web

from metrics_server.handlers.base_metrics_handler import BaseMetricsHandler


class ListMetricsHandler(BaseMetricsHandler):
    def __init__(self, generator_url: str):
        super().__init__("list_metrics", generator_url)

    async def handle(self, request: web.Request) -> web.Response:
        all_metrics = await self._fetch_metrics_from_generator()

        return web.json_response(
            {
                "switches": all_metrics
            }
        )
