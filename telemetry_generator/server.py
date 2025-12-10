# telemetry_generator/server.py
import asyncio
from aiohttp import web
from telemetry_generator.handlers.counters import CountersHandler
from shared.base import BaseRedisStore
from telemetry_generator.telemetry_generator import TelemetryGenerator  # your class
from telemetry_generator.config import AppConfig

def create_app(config: AppConfig) -> web.Application:
    app = web.Application()

    # Redis store shared by handlers
    redis_store = BaseRedisStore(
        config.redis.host,
        config.redis.port,
        config.redis.db,
    )
    app["redis"] = redis_store

    # Register handlers
    counters_handler = CountersHandler(redis_store)
    app.router.add_get("/counters", counters_handler)

    # Create telemetry generator instance
    telemetry_gen = TelemetryGenerator(
        config=config.telemetry,
        redis_store=redis_store,
    )

    # Start background task when app starts
    async def start_background_tasks(app: web.Application):
        app["telemetry_task"] = app.loop.create_task(telemetry_gen.run())

    async def cleanup_background_tasks(app: web.Application):
        task = app["telemetry_task"]
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)

    return app
