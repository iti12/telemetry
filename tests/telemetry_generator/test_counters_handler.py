import csv
import io
import pytest


@pytest.mark.asyncio
async def test_counters_csv_format(client, test_app, monkeypatch):
    fake_metrics = {
        "sw-1": {
            "bandwidth_in": 100,
            "bandwidth_out": 200,
            "latency_ms": 5,
            "packet_errors": 0,
            "updated_at": "2025-01-01T00:00:00",
        }
    }

    def fake_get_all_metrics():
        return fake_metrics

    # ✅ Patch Redis read method
    monkeypatch.setattr(
        test_app["redis"],
        "get_all_metrics",
        fake_get_all_metrics,
    )

    resp = await client.get("/counters")
    assert resp.status == 200
    assert resp.headers["Content-Type"].startswith("text/csv")

    text = await resp.text()
    rows = list(csv.reader(io.StringIO(text)))

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
