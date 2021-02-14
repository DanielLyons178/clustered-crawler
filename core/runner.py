import argparse
from core.engine.comms.output.rabbit_link_writer import RabbitLinkWriter
from core.lib.link_extraction.link_extractor import LinkExtractor
import threading
import importlib
import logging
from core.engine.comms.output.outputter_factory import RabbitOutputterFactory
from core.engine.join_listener import JoinListener
from core.engine.comms.output.visit_cacher import VisitCacher
from core.engine.comms.link_receive.rabbit_reciever import RabbitReciever
from core.engine.scraper_engine import ScraperEngine


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

    link_receiver = RabbitReciever(
        args.rabbit_host,
        args.rabbit_port,
        (args.rabbit_user, args.rabbit_password),
        "links",
    )
    join_receiver = RabbitReciever(
        args.rabbit_host,
        args.rabbit_port,
        (args.rabbit_user, args.rabbit_password),
        "join",
    )
    cacher = VisitCacher(args.redis_host, args.redis_port, args.redis_password)
    engn = ScraperEngine(link_receiver, cacher)
    outputter_factory = RabbitOutputterFactory(
        args.rabbit_host, args.rabbit_port, (args.rabbit_user, args.rabbit_password)
    )

    join_listenter = JoinListener(join_receiver, engn, outputter_factory)
    join_listener_thread = threading.Thread(target=join_listenter.run)

    join_listener_thread.start()
   
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

    link_writer = RabbitLinkWriter(
        args.rabbit_host,
        args.rabbit_port,
        (args.rabbit_user, args.rabbit_password),
        "links",
    )

    joiner = RabbitLinkWriter(
        args.rabbit_host,
        args.rabbit_port,
        (args.rabbit_user, args.rabbit_password),
        "join",
    )
    for (module_str, clazz_str) in module_classes:
        module_str = ".".join(module_str)
        module = importlib.import_module(module_str)
        clazz = getattr(module, clazz_str)

        if not issubclass(clazz, LinkExtractor):
            raise Exception("Must subclass LinkExtractor")

        rec = RabbitReciever(
            args.rabbit_host,
            args.rabbit_port,
            (args.rabbit_user, args.rabbit_password),
            f"{module_str}.{clazz_str}",
        )

        ex = clazz(rec, link_writer, joiner)
        ex.run()


if __name__ == "__main__":
    main()