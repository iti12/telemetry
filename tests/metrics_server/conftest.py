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
    return await aiohttp_client(test_app)
