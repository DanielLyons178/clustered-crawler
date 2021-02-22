from abc import ABC, abstractmethod
import json


class LinkExtractor(ABC):
    def __init__(self, sender) -> None:
        super().__init__()
        self._sender = sender

    def process_links(self, html):
        links = self.extract_links(json.loads(html))
        for link in links:
            self._sender.put(link)

    def run(self):
        self._receiver.poll(self.process_links)

    def register_receiver(self, rec):
        self._receiver = rec

    @abstractmethod
    def extract_links(self, html):
        return []

    @abstractmethod
    def for_links_pattern(self):
        return ''