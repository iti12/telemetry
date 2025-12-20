import pytest
import pytest_asyncio

from telemetry_generator.server import create_app
from base.config import (
    AppConfig,
    GeneratorServerConfig,
    TelemetryConfig,
    LoggingConfig,
    RedisConfig,
)
from base.config import MetricServerConfig


@pytest.fixture
def test_config():
    return AppConfig(
        generator_server=GeneratorServerConfig(host="127.0.0.1", port=0),
        metric_server=MetricServerConfig(host="127.0.0.1", port=0),
        telemetry=TelemetryConfig(
            switches=5,
            update_interval_seconds=1,
        ),
        logging=LoggingConfig(level="INFO", file="/tmp/test.log"),
        redis=RedisConfig(host="127.0.0.1", port=6379),
    )


@pytest_asyncio.fixture
async def test_app(test_config):
    return create_app(test_config)


@pytest_asyncio.fixture
async def client(aiohttp_client, test_app):
    return await aiohttp_client(test_app)
