import argparse
import logging
from aiohttp import web

from base.config import load_config
from metrics_server.server import create_app


def setup_logging(level: str):
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s %(levelname)s %(message)s",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    setup_logging(config.logging.level)

    app = create_app(config)
    web.run_app(app, host=config.metric_server.host, port=config.metric_server.port)


if __name__ == "__main__":
    main()
