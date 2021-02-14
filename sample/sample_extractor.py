


from core.lib.link_extraction.link_extractor import LinkExtractor


class SampleExtractor(LinkExtractor):

    def extract_links(self, html):
        return ['google.com']