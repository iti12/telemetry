import asyncio
import pytest


@pytest.mark.asyncio
async def test_concurrent_requests(client):
    async def fetch():
        resp = await client.get("/counters")
        assert resp.status == 200

    await asyncio.gather(*(fetch() for _ in range(10)))
