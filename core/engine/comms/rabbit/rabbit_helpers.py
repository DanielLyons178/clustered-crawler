import pika
from pika.connection import Connection


def rabbit_blocking_connection_factory(host, port, creds):
    creds = pika.PlainCredentials(creds[0], creds[1])
    params = pika.ConnectionParameters(host, port, credentials=creds)
    def factory():
        return pika.BlockingConnection(params) 
    return factory
