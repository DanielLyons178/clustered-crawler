from bs4 import BeautifulSoup
from scraper.client.lib.body_reader.body_reader import BodyReader


class SampleReader(BodyReader):

    def process_body(self, html):
        soup = BeautifulSoup(html, features="html.parser")
        title = soup.title.string if soup.title else ''
        print(title)        
        return None

    def for_links_pattern(self):
        return ["#"]