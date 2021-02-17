import argparse
from core.engine.comms.output.result_outputter import ResultOutputter
from uuid import uuid4
from core.engine.comms.output.link_writer import LinkWriter
from core.engine.comms.rabbit.rabbit_reciever import RabbitReciever
from core.engine.comms.rabbit.rabbit_outputter import RabbitOutputter
from core.engine.comms.rabbit.rabbit_helpers import rabbit_blocking_connection_factory
from core.engine.comms.output.redis_state_maintainer import RedisStateMaintainer

import redis

from core.engine.comms.redis.redis_cacher import RedisVisitCacher
from core.engine.scraper_engine import ScraperEngine
from core.lib.link_extraction.link_extractor import LinkExtractor
import importlib
import logging



from core.web.server import app


def main():

    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description="Distributed Scraper")

    subs = parser.add_subparsers(dest="mode")
    core_parser = subs.add_parser("core")
    link_extractor = subs.add_parser("links")
    result = subs.add_parser("res")
    server = subs.add_parser("web")

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

    link_extractor.add_argument("--extractors", "-ex")

    args = parser.parse_args()

    if args.mode == "core":
        run_core(args)
    elif args.mode == "links":
        run_link_extractor(args)
    elif args.mode == "web":
        run_web(args)


def run_core(args):

    conn_factory = rabbit_blocking_connection_factory(
        args.rabbit_host,
        args.rabbit_port,
        (args.rabbit_user, args.rabbit_password),
    )
    rabbit_outputter = RabbitOutputter(("result", "topic"), conn_factory)
    result_outputter = ResultOutputter(rabbit_outputter)

    link_receiver = RabbitReciever(
        conn_factory, ("links", "fanout"), str(uuid4()), [""]
    )

    cacher = RedisVisitCacher(args.redis_host, args.redis_port, args.redis_password)
    engn = ScraperEngine(link_receiver, cacher, [result_outputter])

    engn.run()


def run_web(args):
    app.config.update(
        rabbit_host=args.rabbit_host,
        rabbit_port=args.rabbit_port,
        rabbit_user=args.rabbit_user,
        rabbit_password=args.rabbit_password,
        link_queue="links",
    )
    app.run()


def run_link_extractor(args):

    classes = args.extractors.split(",")

    splits = [clazz.split(".") for clazz in classes]
    module_classes = [(split[:-1], split[-1]) for split in splits]

    conn_factory = rabbit_blocking_connection_factory(
        args.rabbit_host,
        args.rabbit_port,
        (args.rabbit_user, args.rabbit_password),
    )

    link_outputter = RabbitOutputter(("links", "fanout"), conn_factory)
    link_writer = LinkWriter(link_outputter)

    for (module_str, clazz_str) in module_classes:
        module_str = ".".join(module_str)
        module = importlib.import_module(module_str)
        clazz = getattr(module, clazz_str)

        if not issubclass(clazz, LinkExtractor):
            raise Exception("Must subclass LinkExtractor")

        ex = clazz(link_writer)
        rec = RabbitReciever(
            conn_factory, ("result", "topic"), f"{module_str}.{clazz_str}", ex.for_links_pattern()
        )
        ex.register_receiver(rec)
        ex.run()


if __name__ == "__main__":
    main()