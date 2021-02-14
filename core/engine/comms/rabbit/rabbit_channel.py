import pika


class RabbitChannel:
    def __init__(self, host, port, creds) -> None:
        super().__init__()
        creds = pika.PlainCredentials(creds[0], creds[1])
        params = pika.ConnectionParameters(host, port, credentials=creds)
        conn = pika.BlockingConnection(params)
        self.chnl = conn.channel()

    def basic_consume(self, queue, callback, *args, **kwargs):
        self._init_queue(queue)
        cb = lambda x, y, z, body: callback(body)
        self.chnl.basic_consume(queue, cb, *args, **kwargs)
        self.chnl.start_consuming()

    def basic_publish(self, *args, **kwargs):
        self._init_queue(kwargs["routing_key"])
        self.chnl.basic_publish(
            *args,
            **kwargs,
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

    def _init_queue(self, queue):
        self.chnl.queue_declare(queue, durable=True)