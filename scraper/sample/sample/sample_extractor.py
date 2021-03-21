from bs4 import BeautifulSoup
from bs4.element import SoupStrainer
from scraper.client.lib.link_extraction.link_extractor import LinkExtractor


class SampleExtractor(LinkExtractor):
    def extract_links(self, result):
        soup = BeautifulSoup(result['res'], parse_only=SoupStrainer("a"), features="html.parser")
        return [
            link["href"]
            for link in soup.find_all(attrs={"class": "storylink"})
            if link.has_attr("href")
        ]

    def for_links_pattern(self):
        return ["news.ycombinator.com.#"]