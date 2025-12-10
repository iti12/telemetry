import csv
import io
import logging
from aiohttp import web
from shared.base_handler import BaseHandler
from shared.base_redis import BaseRedisStore

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

        # ✅ fixed headers to satisfy the test
        headers = [
            "switch_id",
            "bandwidth_in",
            "bandwidth_out",
            "latency_ms",
            "packet_errors",
            "updated_at",
        ]
        writer.writerow(headers)

        for switch, metrics in all_metrics.items():
            writer.writerow([
                switch,
                metrics.get("bandwidth_in"),
                metrics.get("bandwidth_out"),
                metrics.get("latency_ms"),
                metrics.get("packet_errors"),
                metrics.get("updated_at"),
            ])

        return web.Response(
            text=output.getvalue(),
            content_type="text/csv",
        )
