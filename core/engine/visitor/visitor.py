import requests

class Visitor:

    def __init__(self) -> None:
        self.sess = requests.session()

    def get(self, link):
        res = self.sess.get(link)
        return res.text