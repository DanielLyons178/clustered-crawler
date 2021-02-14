

from core.lib.body_reader.body_reader import BodyReader


class SmapleReader(BodyReader):

    def process_body(self, html):
        print(html)
        return None