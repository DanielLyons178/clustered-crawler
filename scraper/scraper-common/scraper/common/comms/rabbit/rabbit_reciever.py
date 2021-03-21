from typing import Callable
from pika.connection import Connection


class RabbitReciever:
    def __init__(
        self,
        rabbit_conn_factory: Callable[[], Connection],
        exchange,
        queue_name,
        bindings=[],
    ) -> None:
        super().__init__()
        (exchange_name, exchange_type) = exchange
        self.conn = rabbit_conn_factory()
        self.chnl = self.conn.channel()
        self.chnl.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
        self.chnl.queue_declare(queue_name, durable=True)
        self.queue = queue_name
        for binding in bindings:
            self.chnl.queue_bind(
                exchange=exchange_name, queue=queue_name, routing_key=binding
            )
      

    def poll(self, callback):
        self.chnl.basic_consume(
            self.queue,
            lambda ch, method, properties, body: callback(body),
            auto_ack=True,
        )
        self.chnl.start_consuming()