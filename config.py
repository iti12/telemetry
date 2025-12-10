import yaml
from dataclasses import dataclass

@dataclass
class RedisConfig:
    host: str
    port: int
    db: int = 0

@dataclass(frozen=True)
class ServerConfig:
    host: str
    port: int


@dataclass(frozen=True)
class TelemetryConfig:
    switches: int
    update_interval_seconds: int


@dataclass(frozen=True)
class LoggingConfig:
    level: str
    file: str


@dataclass(frozen=True)
class AppConfig:
    generator_server: ServerConfig
    telemetry: TelemetryConfig
    logging: LoggingConfig
    redis: RedisConfig

def load_config(path: str) -> AppConfig:
    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    return AppConfig(
        generator_server=ServerConfig(**raw["generator_server"]),
        telemetry=TelemetryConfig(**raw["telemetry"]),
        logging=LoggingConfig(**raw["logging"]),
        redis=RedisConfig(**raw["redis"]),
    )
