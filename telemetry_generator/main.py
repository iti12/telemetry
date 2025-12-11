import argparse
import logging

from shared.config import load_config
from telemetry_generator.server import create_app


def setup_logging(level: str, logfile: str):
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(logfile),
        ],
    )
    logging.getLogger("aiohttp.access").setLevel(logging.WARNING)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    setup_logging(config.logging.level, config.logging.file)

    from aiohttp import web
    app = create_app(config)

    web.run_app(app, host=config.generator_server.host, port=config.generator_server.port)

if __name__ == "__main__":
    main()
