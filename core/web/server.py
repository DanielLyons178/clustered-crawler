from flask import Flask, request
from core.engine.comms.output.rabbit_link_writer import RabbitLinkWriter

app = Flask(__name__)


@app.route("/", methods=["POST"])
def post_link():
    connection = RabbitLinkWriter(
        app.config.get("rabbit_host"),
        app.config.get("rabbit_port"),
        (app.config.get("rabbit_user"), app.config.get("rabbit_password")),
        app.config.get("link_queue"),
    )

    connection.put(request.json["link"])

    return ("", 204)
