import argparse

import os
from .engine.comms.output.result_outputter import ResultOutputter
from scraper.common.comms.rabbit.rabbit_reciever import RabbitReciever
from scraper.common.comms.rabbit.rabbit_outputter import RabbitOutputter
from scraper.common.comms.rabbit.rabbit_helpers import (
    rabbit_blocking_connection_factory,
)
from .engine.comms.redis.redis_cacher import RedisVisitCacher
from .engine.scraper_engine import ScraperEngine
import logging


def main():

    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description="Distributed Scraper")

    opts = [
        ("--rabbit_host", "-rh", os.environ.get('RABBIT_HOST')),
        ("--rabbit_port", "-rp", os.environ.get('RABBIT_PORT', '5672')),
        ("--rabbit_user", "-ru", os.environ.get('RABBIT_USER')),
        ("--rabbit_password", "-rpwd", os.environ.get('RABBIT_PASS')),
    ]

    for opt in opts:
        parser.add_argument(opt[0], opt[1], default=opt[2])

    redis_group = parser.add_argument_group("redis")
    redis_group.add_argument("--redis_host", "-redh", default=os.environ.get('REDIS_HOST'))
    redis_group.add_argument("--redis_port", "-redp", default=os.environ.get('REDIS_PORT'))
    redis_group.add_argument("--redis_password", "-redpwd", default=os.environ.get('REDIS_PASS'))

    args = parser.parse_args()
    run_core(args)


def run_core(args):

    conn_factory = rabbit_blocking_connection_factory(
        args.rabbit_host,
        args.rabbit_port,
        (args.rabbit_user, args.rabbit_password),
    )
    rabbit_outputter = RabbitOutputter(("result", "topic"), conn_factory)
    result_outputter = ResultOutputter(rabbit_outputter)

    link_receiver = RabbitReciever(
        conn_factory, ("links", "direct"), "links", ["links"]
    )

    cacher = RedisVisitCacher(args.redis_host, args.redis_port, args.redis_password)
    engn = ScraperEngine(link_receiver, cacher, [result_outputter])

    engn.run()


if __name__ == "__main__":
    main()