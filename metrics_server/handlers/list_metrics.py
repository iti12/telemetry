from aiohttp import web
from shared.base_handler import BaseHandler
from shared.base_redis import BaseRedisStore


class ListMetricsHandler(BaseHandler):
    def __init__(self, redis_store: BaseRedisStore):
        super().__init__("list_metrics")
        self.redis = redis_store

    async def handle(self, request: web.Request) -> web.Response:
        all_metrics = self.redis.get_all_metrics()

        return web.json_response(
            {
                "switches": all_metrics
            }
        )
