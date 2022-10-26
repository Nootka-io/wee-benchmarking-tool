from goose3 import Goose
from wee_cli.extractors import BaseExtractor

class Goose3Extract(BaseExtractor):

    name = 'goose3'

    @staticmethod
    def extract(html):
        try:
            g = Goose()
            article = g.extract(raw_html=html)
            res = article.cleaned_text
        except:
            return ''
        return res
