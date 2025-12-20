from aiohttp import web

from metrics_server.handlers.base_metrics_handler import BaseMetricsHandler


class GetMetricHandler(BaseMetricsHandler):
    def __init__(self, generator_url: str):
        super().__init__("get_metric", generator_url)

    async def handle(self, request: web.Request) -> web.Response:
        switch_id = request.match_info["switch_id"]
        metric = request.match_info["metric"]

        all_metrics = await self._fetch_metrics_from_generator()

        if switch_id not in all_metrics:
            raise web.HTTPNotFound(text=f"Switch '{switch_id}' not found")

        switch_metrics = all_metrics[switch_id]

        if metric not in switch_metrics:
            raise web.HTTPNotFound(
                text=f"Metric '{metric}' not found for switch '{switch_id}'"
            )

        return web.json_response(
            {
                "switch_id": switch_id,
                "metric": metric,
                "value": switch_metrics[metric],
            }
        )
