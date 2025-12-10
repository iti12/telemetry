import redis
print(redis.__file__)
from typing import Dict, Any, List


class BaseRedisStore:
    KEY_PREFIX = "telemetry"

    def __init__(self, host: str, port: int, db: int):
        self._redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )

    def _switch_key(self, switch_id: str) -> str:
        return f"{self.KEY_PREFIX}:{switch_id}"

    # ---- Sync methods ----

    def set_switch_metrics(self, switch_id: str, metrics: Dict[str, Any]):
        self._redis.hset(self._switch_key(switch_id), mapping=metrics)

    def get_switch_metrics(self, switch_id: str) -> Dict[str, Any]:
        return self._redis.hgetall(self._switch_key(switch_id))

    def list_switches(self) -> List[str]:
        keys = self._redis.keys(f"{self.KEY_PREFIX}:*")
        return [k.split(":", 1)[1] for k in keys]

    def get_all_metrics(self) -> Dict[str, Dict[str, Any]]:
        result = {}
        for switch_id in self.list_switches():
            result[switch_id] = self.get_switch_metrics(switch_id)
        return result

    def close(self):
        self._redis.close()
