import time
import logging
from abc import ABC, abstractmethod
from aiohttp import web

logger = logging.getLogger(__name__)


class BaseHandler(ABC):
    def __init__(self, name: str):
        self.name = name
        self.request_count = 0
        self.total_latency = 0.0

    async def __call__(self, request: web.Request) -> web.Response:
        start = time.perf_counter()
        self.request_count += 1
        try:
            return await self.handle(request)
        except Exception:
            logger.exception("Handler error")
            raise web.HTTPInternalServerError()
        finally:
            self.total_latency += time.perf_counter() - start
            logger.info(f"{request.method} {self.name} metrics: avg_latency={self.avg_latency:.3f}s, requests={self.request_count}")

    @abstractmethod
    async def handle(self, request: web.Request) -> web.Response:
        pass

    @property
    def avg_latency(self):
        return self.total_latency / self.request_count if self.request_count else 0.0
