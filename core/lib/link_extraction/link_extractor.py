from abc import ABC, abstractmethod
import json


class LinkExtractor(ABC):
    def __init__(self, receiver, sender, joiner) -> None:
        super().__init__()
        self._sender = sender
        self._joiner = joiner
        self._receiver = receiver

    def process_links(self, html):
        links = self.extract_links(html)
        for link in links:
            self._sender.put(link)

    def run(self):
        queue_name = f"{self.__class__.__module__}.{self.__class__.__name__}"
        join_props = {"queue": queue_name, "type": "LinkExtractor"}
        self._joiner.put(json.dumps(join_props))
        self._receiver.poll(self.process_links)

    @abstractmethod
    def extract_links(self, html):
        return []