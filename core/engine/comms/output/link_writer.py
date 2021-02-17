class LinkWriter:
    def __init__(self, outputter) -> None:
        self.outputter = outputter

    def put(self, link):
        self.outputter.put(link)
