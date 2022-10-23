from extractors import BaseExtractor
from resiliparse.parse.html import HTMLTree
from resiliparse.extract.html2text import extract_plain_text


class ResiliparsePlainExtract(BaseExtractor):

    name = 'resiliparse-plain'

    @staticmethod
    def extract(html):
        try:
            tree = HTMLTree.parse(html)
            article = extract_plain_text(tree)
            res = article

        except Exception as e:
            return ''
        return res
