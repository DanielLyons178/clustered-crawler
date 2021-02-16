class RedisStateMaintainer:
    def __init__(self, client) -> None:
        self.client = client

    def set_master(self):
        self.client.set("master", True)

    def has_master(self):
        return self.client.get("master") == "true"

    def register_outputter(self, outputter_queue):
        self.client.sadd("outputters", outputter_queue)

    def deregister_outputter(self, outputter_queue):
        self.client.srem("outputters", outputter_queue)

    def get_outputters(self):
        return self.client.smembers("outputters")