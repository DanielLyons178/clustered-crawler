import redis


class VisitCacher:

    HASH = "visits"

    def __init__(self, host, port, pwd) -> None:
        self.client = redis.StrictRedis(host=host, port=port, db=0, password=pwd)

    def put(self, link):
        self.client.hset(self.HASH, link)

    def is_visited(self, link):
        return self.client.hexists(self.HASH, link)