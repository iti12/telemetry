import pytest


@pytest.mark.asyncio
async def test_metrics(client):
    r = await client.get("/metrics")
    assert r.status == 200
    data = await r.json()
    assert "switches" in data
