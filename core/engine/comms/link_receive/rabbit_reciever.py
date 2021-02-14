from core.engine.comms.rabbit.rabbit_channel import RabbitChannel


class RabbitReciever:
    def __init__(self, host, port, creds, queue_name) -> None:
        super().__init__()
        self.queue = queue_name
        self.chnl = RabbitChannel(host, port, creds)
        

    def poll(self, callback):
        self.chnl.basic_consume(self.queue, callback, auto_ack=True)