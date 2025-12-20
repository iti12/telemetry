import asyncio
import random
from base.base_redis import BaseRedisStore
from base.config import TelemetryConfig


class DataGenerator:
    def __init__(self, config: TelemetryConfig, redis_store: BaseRedisStore):
        self.config = config
        self.redis = redis_store

    async def run(self):
        while True:
            for i in range(self.config.switches):
                switch_id = f"switch-{i}"

                metrics = {
                    "bandwidth_mbps": round(random.uniform(10, 100), 2),
                    "latency_ms": round(random.uniform(0.1, 10), 2),
                    "packet_errors": random.randint(0, 10),
                }

                self.redis.set_switch_metrics(switch_id, metrics)

            await asyncio.sleep(self.config.update_interval_seconds)
