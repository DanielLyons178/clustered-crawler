import json


class RabbitOutputter:
    def __init__(self, exchange, rabbit_conn_factory) -> None:
        super().__init__()
        (exchange_name, exchange_type) = exchange
        self.conn = rabbit_conn_factory()
        self.exchange = exchange_name
        self.chnl = self.conn.channel()
        self.chnl.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

    def put(self, msg, recipient=""):
        content_string = json.dumps(msg) if not isinstance(msg, str) else msg
        self.chnl.basic_publish(
            exchange=self.exchange, routing_key=recipient, body=content_string
        )
