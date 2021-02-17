from abc import ABC, abstractmethod


class VisitRecorder(ABC):

    @abstractmethod
    def put(self, link):
        self.client.sadd(self.HASH, link)

    @abstractmethod
    def is_visited(self, link):
        return self.client.sismember(self.HASH, link)