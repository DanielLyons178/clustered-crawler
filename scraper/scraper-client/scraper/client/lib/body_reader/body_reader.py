from abc import ABC, abstractmethod
import logging

class BodyReader(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger("Body Reader")


    def run(self):
        self.logger.info("Waiting to extract content")
        self._receiver.poll(self.process_body)

    def register_receiver(self, rec):
        self._receiver = rec

    @abstractmethod
    def process_body(self, html):
        return None

    @abstractmethod 
    def for_links_pattern(self):
        return ['#']