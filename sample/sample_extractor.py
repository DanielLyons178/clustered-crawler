


from core.lib.link_extraction.link_extractor import LinkExtractor


class SampleExtractor(LinkExtractor):

    def extract_links(self, html):
        return ['https://google.com']

    def for_links_pattern(self):
        return ["www.google.com.#"]