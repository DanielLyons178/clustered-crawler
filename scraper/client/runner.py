import importlib
import argparse
from scraper.client.lib.body_reader.body_reader import BodyReader
from scraper.client.link_writer import LinkWriter
from scraper.common.comms.rabbit.rabbit_outputter import RabbitOutputter
from scraper.common.comms.rabbit.rabbit_reciever import RabbitReciever
from scraper.client.lib.link_extraction.link_extractor import LinkExtractor
from scraper.common.comms.rabbit.rabbit_helpers import (
    rabbit_blocking_connection_factory,
)


def main():

    parser = argparse.ArgumentParser(description="Distributed Scraper")
    subs = parser.add_subparsers(dest="mode")

    add_modes(subs)

    opts = [
        ("--rabbit_host", "-rh"),
        ("--rabbit_port", "-rp"),
        ("--rabbit_user", "-ru"),
        ("--rabbit_password", "-rpwd"),
    ]

    for opt in opts:
        parser.add_argument(opt[0], opt[1])

    args = parser.parse_args()

    if args.mode == "links":
        run_link_extractor(args)
    elif args.mode == "body":
        run_result_processor(args)

def add_modes(subs):
    link_extractor = subs.add_parser("links")
    link_extractor.add_argument("--extractors", "-ex")

    body_reader = subs.add_parser("body")
    body_reader.add_argument("--body_readers", "-br")


def run_link_extractor(args):

    classes = args.extractors.split(",")

    splits = [clazz.split(".") for clazz in classes]
    module_classes = [(split[:-1], split[-1]) for split in splits]

    conn_factory = rabbit_blocking_connection_factory(
        args.rabbit_host,
        args.rabbit_port,
        (args.rabbit_user, args.rabbit_password),
    )

    link_outputter = RabbitOutputter(("links", "direct"), conn_factory)
    link_writer = LinkWriter(link_outputter)

    for (module_str, clazz_str) in module_classes:
        module_str = ".".join(module_str)
        module = importlib.import_module(module_str)
        clazz = getattr(module, clazz_str)

        if not issubclass(clazz, LinkExtractor):
            raise Exception("Must subclass LinkExtractor")

        ex = clazz(link_writer)
        rec = RabbitReciever(
            conn_factory,
            ("result", "topic"),
            f"{module_str}.{clazz_str}",
            ex.for_links_pattern(),
        )
        ex.register_receiver(rec)
        ex.run()


def run_result_processor(args):
    classes = args.body_readers.split(",")
    splits = [clazz.split(".") for clazz in classes]
    module_classes = [(split[:-1], split[-1]) for split in splits]

    conn_factory = rabbit_blocking_connection_factory(
        args.rabbit_host,
        args.rabbit_port,
        (args.rabbit_user, args.rabbit_password),
    )

    for (module_str, clazz_str) in module_classes:
        module_str = ".".join(module_str)
        module = importlib.import_module(module_str)
        clazz = getattr(module, clazz_str)

        if not issubclass(clazz, BodyReader):
            raise Exception("Must subclass LinkExtractor")

        body_reader = clazz()
        rec = RabbitReciever(
            conn_factory,
            ("result", "topic"),
            f"{module_str}.{clazz_str}",
            body_reader.for_links_pattern(),
        )
        body_reader.register_receiver(rec)
        body_reader.run()


if __name__ == "__main__":
    main()