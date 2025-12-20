import pytest
from aiohttp import web


@pytest.mark.asyncio
async def test_get_metric(client, monkeypatch):
    fake_data = {
        "switch-1": {
            "latency_ms": "1.23",
            "bandwidth_mbps": "10.5",
        }
    }

    async def fake_fetch(self):
        return fake_data

    monkeypatch.setattr(
        "metrics_server.handlers.get_metric.BaseMetricsHandler._fetch_metrics_from_generator",
        fake_fetch,
    )

    resp = await client.get("/telemetry/switch-1/latency_ms")
    assert resp.status == 200

    data = await resp.json()
    assert data == {
        "switch_id": "switch-1",
        "metric": "latency_ms",
        "value": "1.23",
    }
