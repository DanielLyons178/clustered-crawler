from .visitor.visitor import Visitor
import logging


class ScraperEngine:
    def __init__(
        self, link_reciever, visit_cacher, result_outputters=[]
    ) -> None:
        self.visitor = Visitor()
        self.link_reciever = link_reciever
        self.result_outputters = result_outputters
        self.visit_cacher = visit_cacher
        self.logger = logging.getLogger("Engine")

    def run(self):
        self.logger.info("Listening for links")
        self.link_reciever.poll(self.process_link)

    def process_link(self, link):
        self.logger.info("Processing link %s", link)
        if not self.visit_cacher.is_visited(link):
            result = self.visitor.get(link)
            for outputter in self.result_outputters:
                outputter.put((link, result))
            self.visit_cacher.put(link)
