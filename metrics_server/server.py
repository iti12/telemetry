from aiohttp import web
from shared.config import AppConfig
from metrics_server.handlers.get_metric import GetMetricHandler
from metrics_server.handlers.list_metrics import ListMetricsHandler


def create_app(config: AppConfig) -> web.Application:
    app = web.Application()

    generator_url = f"http://{config.generator_server.host}:{config.generator_server.port}"

    app.router.add_get(
        "/telemetry/",
        ListMetricsHandler(generator_url),
    )
    app.router.add_get(
        "/telemetry/{switch_id}/{metric}",
        GetMetricHandler(generator_url),
    )
    return app
