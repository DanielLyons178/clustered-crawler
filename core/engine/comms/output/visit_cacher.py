import redis

class VisitCacher():

    def __init__(self, host, port, pwd) -> None:
        self.client = redis.StrictRedis(host=host, port=port,db=0, password=pwd)
        
        
    def put(self, link):
        self.client.set(link, 1)

    def is_visited(self, link):
        return self.client.exists(link)