from core.engine.comms.output.link_writer import LinkWriter
from core.engine.comms.rabbit.rabbit_outputter import RabbitOutputter
from core.engine.comms.rabbit.rabbit_helpers import rabbit_blocking_connection_factory
from flask import Flask, request

app = Flask(__name__)




@app.route("/", methods=["POST"])
def post_link():
   # app.config.get("link_queue"),
    conn_factory = rabbit_blocking_connection_factory(
        app.config.get("rabbit_host"),
        app.config.get("rabbit_port"),
        (app.config.get("rabbit_user"), app.config.get("rabbit_password")),
    )

    link_outputter = RabbitOutputter("links", conn_factory)
    link_writer = LinkWriter(link_outputter)
    return ("", 204)
