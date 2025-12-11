import pytest


@pytest.mark.asyncio
async def test_list_metrics(client):
    resp = await client.get("/telemetry/")
    assert resp.status == 200

    data = await resp.json()
    assert "switches" in data
    assert "sw-1" in data["switches"]
