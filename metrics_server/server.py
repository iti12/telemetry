from aiohttp import web
from shared.config import AppConfig
from shared.base_redis import BaseRedisStore
from metrics_server.handlers.get_metric import GetMetricHandler
from metrics_server.handlers.list_metrics import ListMetricsHandler


def create_app(config: AppConfig) -> web.Application:
    app = web.Application()

    redis_store = BaseRedisStore(
        config.redis.host,
        config.redis.port,
        config.redis.db,
    )
    app["redis"] = redis_store

    app.router.add_get(
        "/telemetry/",
        ListMetricsHandler(redis_store),
    )
    app.router.add_get(
        "/telemetry/{switch_id}/{metric}",
        GetMetricHandler(redis_store),
    )

    return app
