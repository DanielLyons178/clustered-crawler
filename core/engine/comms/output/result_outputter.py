import json
from urllib import parse


class ResultOutputter:
    def __init__(self, outputter) -> None:
        super().__init__()
        self.outputter = outputter

    def put(self, result):
        (link, res) = result
        content = {'link': link.decode('utf-8'), 'res': res}
        parsed = parse.urlparse(link)

        recipient = f"{parsed.hostname.decode('utf-8')}{parsed.path.decode('utf-8').replace('/', '.')}"
        content_string = json.dumps(content)
        self.outputter.put(content_string, recipient)
