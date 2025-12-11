import pytest
import pytest_asyncio

from metrics_server.server import create_app
from shared.config import (
    AppConfig,
    GeneratorServerConfig,
    MetricServerConfig,
    TelemetryConfig,
    LoggingConfig,
    RedisConfig,
)


@pytest.fixture
def test_config():
    return AppConfig(
        generator_server=GeneratorServerConfig(host="127.0.0.1", port=0),
        metric_server=MetricServerConfig(host="127.0.0.1", port=0),
        telemetry=TelemetryConfig(switches=1, update_interval_seconds=1),
        logging=LoggingConfig(level="INFO", file="/tmp/test.log"),
        redis=RedisConfig(host="127.0.0.1", port=6379),
    )


@pytest_asyncio.fixture
async def test_app(test_config):
    app = create_app(test_config)
    return app


@pytest_asyncio.fixture
async def client(aiohttp_client, test_app):
    redis = test_app["redis"]
    redis.set_metrics(
        "sw-1",
        {
            "bandwidth_in": 100,
            "bandwidth_out": 200,
            "latency_ms": 5,
            "packet_errors": 0,
            "updated_at": "2025-01-01T00:00:00",
        },
    )
    return await aiohttp_client(test_app)
