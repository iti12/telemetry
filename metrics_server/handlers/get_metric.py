from aiohttp import web
from shared.base_handler import BaseHandler
from shared.base_redis import BaseRedisStore


class GetMetricHandler(BaseHandler):
    def __init__(self, redis_store: BaseRedisStore):
        super().__init__("get_metric")
        self.redis = redis_store

    async def handle(self, request: web.Request) -> web.Response:
        switch_id = request.match_info.get("switch_id")
        metric = request.match_info.get("metric")

        metrics = await self.redis.get_metrics(switch_id)
        if not metrics or metric not in metrics:
            raise web.HTTPNotFound(
                text=f"Metric '{metric}' not found for switch '{switch_id}'"
            )

        return web.json_response(
            {
                "switch_id": switch_id,
                "metric": metric,
                "value": metrics[metric],
            }
        )
