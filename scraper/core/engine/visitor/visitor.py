import requests
import logging

class Visitor:
    def __init__(self) -> None:
        self.sess = requests.session()
        self.logger = logging.getLogger("Visitor")


    def get(self, link):
        try:
            res = self.sess.get(
                link,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
                },
                timeout=10,
            )
            return res.text
        except:
            self.logger.warn("Failed to visit link %s", link)
            return ''