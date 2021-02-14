from core.engine.comms.rabbit.rabbit_channel import RabbitChannel
import json


class RabbitResultOutputter():
    def __init__(self, host, port, creds, queue_name) -> None:
        super().__init__()
        self.queue = queue_name
        self.chnl = RabbitChannel(host, port, creds)

    def put(self, result):
        (link, res) = result
        content = {link: link, res: res}
        content_string = json.dumps(content)
        self.chnl.basic_publish(
            exchange="", routing_key=self.queue, body=content_string
        )
