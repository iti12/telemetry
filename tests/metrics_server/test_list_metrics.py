import pytest


@pytest.mark.asyncio
async def test_list_metrics(client, monkeypatch):
    fake_data = {
        "switch-1": {"latency_ms": "1.23"},
        "switch-2": {"latency_ms": "4.56"},
    }

    async def fake_fetch(self):
        return fake_data

    monkeypatch.setattr(
        "metrics_server.handlers.list_metrics.BaseMetricsHandler._fetch_metrics_from_generator",
        fake_fetch,
    )

    resp = await client.get("/telemetry/")
    assert resp.status == 200

    data = await resp.json()
    assert data == {"switches": fake_data}
