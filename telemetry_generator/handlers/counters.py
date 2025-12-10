import csv
import io
import logging
from aiohttp import web
from telemetry_generator.handlers.base import BaseHandler
from shared.base import BaseRedisStore

logger = logging.getLogger(__name__)

class CountersHandler(BaseHandler):
    def __init__(self, redis_store: BaseRedisStore):
        super().__init__("counters")
        self.redis = redis_store

    async def handle(self, request: web.Request) -> web.Response:
        all_metrics = self.redis.get_all_metrics()
        if not all_metrics:
            logger.info(f"no metrics")
            return web.Response(text="", content_type="text/csv")

        output = io.StringIO()
        writer = csv.writer(output)

        headers = ["switch"] + list(next(iter(all_metrics.values())).keys())
        writer.writerow(headers)

        for switch, metrics in all_metrics.items():
            writer.writerow([switch] + list(metrics.values()))

        return web.Response(
            text=output.getvalue(),
            content_type="text/csv",
        )

