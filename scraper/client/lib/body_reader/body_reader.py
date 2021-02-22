from abc import ABC, abstractmethod


class BodyReader(ABC):
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        self._receiver.poll(self.process_body)

    def register_receiver(self, rec):
        self._receiver = rec

    @abstractmethod
    def process_body(self, html):
        return None

    @abstractmethod 
    def for_links_pattern(self):
        return ['#']