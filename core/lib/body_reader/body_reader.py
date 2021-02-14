from abc import ABC, abstractmethod


class BodyReader(ABC):
    def __init__(self, receiver) -> None:
        super().__init__()
        self._receiver = receiver

    def run(self):
        self._receiver.poll(self.process_body)

    @abstractmethod
    def process_body(self, html):
        return None