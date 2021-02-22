import argparse

from scraper.client.runner import run_link_extractor, add_modes, run_result_processor

from scraper.core.engine.comms.output.result_outputter import ResultOutputter
from scraper.common.comms.rabbit.rabbit_reciever import RabbitReciever
from scraper.common.comms.rabbit.rabbit_outputter import RabbitOutputter
from scraper.common.comms.rabbit.rabbit_helpers import (
    rabbit_blocking_connection_factory,
)
from scraper.core.engine.comms.redis.redis_cacher import RedisVisitCacher
from scraper.core.engine.scraper_engine import ScraperEngine
import logging


def main():

    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description="Distributed Scraper")

    subs = parser.add_subparsers(dest="mode")
    core_parser = subs.add_parser("core")

    add_modes(subs)

    opts = [
        ("--rabbit_host", "-rh"),
        ("--rabbit_port", "-rp"),
        ("--rabbit_user", "-ru"),
        ("--rabbit_password", "-rpwd"),
    ]

    for opt in opts:
        parser.add_argument(opt[0], opt[1])

    redis_group = core_parser.add_argument_group("redis")
    redis_group.add_argument("--redis_host", "-rh")
    redis_group.add_argument("--redis_port", "-rp")
    redis_group.add_argument("--redis_password", "-rpwd")

    args = parser.parse_args()

    if args.mode == "core":
        run_core(args)
    elif args.mode == "links":
        run_link_extractor(args)
    elif args.mode == "body":
        run_result_processor(args)


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