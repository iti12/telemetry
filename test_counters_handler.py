import csv
import io
import pytest


@pytest.mark.asyncio
async def test_counters_csv_format(client):
    resp = await client.get("/counters")
    assert resp.status == 200
    assert resp.headers["Content-Type"].startswith("text/csv")

    text = await resp.text()
    rows = list(csv.reader(io.StringIO(text)))

    # header + data rows
    assert len(rows) > 1

    assert rows[0] == [
        "switch_id",
        "bandwidth_in",
        "bandwidth_out",
        "latency_ms",
        "packet_errors",
        "updated_at",
    ]

    assert rows[1][0].startswith("sw")
