import json
import logging


class JoinListener:
    def __init__(self, receiver, scraper_engine, outputter_factory) -> None:
        self.receiver = receiver
        self.engine = scraper_engine
        self.outputter_factory = outputter_factory

    def run(self):
        logging.getLogger("Joiner").info("Listening for cluster joins")
        self.receiver.poll(self._add)

    def _add(self, msg):
        msg = json.loads(msg)
        q = msg["queue"]
        if not self.engine.is_registered(q):
            outputter = self.outputter_factory.create(q)
            self.engine.join(outputter)