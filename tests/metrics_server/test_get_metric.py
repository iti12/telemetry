import pytest


@pytest.mark.asyncio
async def test_get_metric(client):
    resp = await client.get("/telemetry/sw-1/latency_ms")
    assert resp.status == 200

    data = await resp.json()
    assert data["switch_id"] == "sw-1"
    assert data["metric"] == "latency_ms"
    assert data["value"] == 5
