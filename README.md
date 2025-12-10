# Telemetry Aggregation System

## Overview

This project implements a simulated network telemetry aggregation system inspired by NVIDIA's UFM. It consists of two main components:

1. **Telemetry Generator**: Simulates telemetry data (bandwidth, latency, packet errors) for multiple switches and stores the data in a Redis server.
2. **Telemetry Web Server**: Provides a REST API to fetch telemetry data from Redis. Supports endpoints to get individual metrics or all metrics across switches.

---

## Features

- Simulated telemetry data with configurable update interval.
- Redis-based shared storage for metrics.
- Fast API responses with minimal latency.
- Non-blocking handlers for concurrent requests.
- Basic observability: logs request latency and API activity.
- Configurable server settings (host, port, logging, Redis, etc.).

---

## Directory Structure

telemetry/
├── telemetry_generator/        # Telemetry generator server
│   ├── init.py
│   ├── main.py                 # Entrypoint for telemetry generator
│   ├── telemetry_generator.py  # TelemetryGenerator class
│   ├── server.py               # aiohttp app setup
│   ├── handlers/
│   │   ├── base.py             # BaseHandler class for latency tracking
│   │   └── counters.py         # CountersHandler class
├── shared /            # Shared helper classes
│   ├── init.py
│   └── base.py                 # BaseRedisStore class
├── config.py                   # AppConfig, ServerConfig, TelemetryConfig, RedisConfig
├── setup.py                    # Project dependencies (aiohttp, redis, pytest)
├── tests/                      # Unit tests
└── README.md

---

## Installation

1. Clone the repository:

```bash
git clone <repo-url>
cd telemetry
```

2.	Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```
3.	Install dependencies in editable mode:
```bash
pip install -e .
```
4. Install and Start a Redis server with brew (default host: 127.0.0.1, port: 6379):
```bash
brew install redis
brew services start redis
```

⸻

## Configuration

use config.yaml to config your

    generator_server: (host="127.0.0.1", port=9001),
    telemetry: (switches=5, update_interval_seconds=10),
    logging: (level="INFO", file="/tmp/telemetry.log"),
    redis: (host="127.0.0.1", port=6379, db=0)

⸻

## Running the Telemetry Generator

```bash
python telemetry_generator/main.py
```

*	This starts generating telemetry data for all configured switches and pushes it to Redis.
*	Logs request latency and metrics information to the configured log file.
* enables REST server implementing GET http://127.0.0.1:9001/counters to retrieve all counters

⸻

API Endpoints (for Telemetry Web Server)
	1.	GetMetric: Fetch a specific metric for a specific switch

GET /metrics/{switch_id}/{metric_name}

	2.	ListMetrics: Fetch all metrics for all switches

GET /counters

	•	Returns CSV format: switch,metric1,metric2,...

⸻

## Testing

Run unit tests with:

```bash
pytest -v
```
* The tests cover handlers, concurrency, Redis integration, and telemetry generation.

⸻

## Limitations
	•	Single Redis instance (no clustering or high availability)
	•	Telemetry generator is simulated; no real switch integration
	•	No authentication or rate limiting on API
	•	Scaling beyond a few hundred switches may require optimization

⸻

## Future Improvements
	•	Use asyncio Redis client for high-throughput ingestion
	•	Add caching or batching to reduce Redis load
	•	Implement distributed telemetry generation across multiple nodes
	•	Add authentication and API rate limiting
	•	Collect more observability metrics (histograms, error rates)

This README explains the **system architecture, usage, testing, and future improvements**.  


