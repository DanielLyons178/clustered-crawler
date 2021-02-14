from core.engine.comms.rabbit.rabbit_channel import RabbitChannel


class RabbitLinkWriter:
    def __init__(self, host, port, creds, queue_name="links") -> None:
        self.chnl = RabbitChannel(host, port, creds)
        self.queue = queue_name

    def put(self, link):
        self.chnl.basic_publish(exchange="", routing_key=self.queue, body=link)
