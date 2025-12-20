import logging
import csv
import io
from aiohttp import web, ClientSession

from shared.base_handler import BaseHandler

logger = logging.getLogger(__name__)


class BaseMetricsHandler(BaseHandler):
    def __init__(self, name: str, generator_url: str):
        super().__init__(name)
        self.generator_url = generator_url.rstrip("/")

    async def _fetch_metrics_from_generator(self) -> dict:
        """
        Fetch CSV from generator and return:
        {
            "switch-1": { "latency_ms": "1.23", ... },
            ...
        }
        """
        url = f"{self.generator_url}/counters"

        async with ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise web.HTTPBadGateway(
                        text="Failed to fetch metrics from generator"
                    )

                csv_text = await resp.text()

        reader = csv.DictReader(io.StringIO(csv_text))
        result = {}

        for row in reader:
            switch_id = row.pop("switch_id")
            result[switch_id] = row

        return result
