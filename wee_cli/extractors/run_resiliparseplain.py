from wee_cli.extractors import BaseExtractor
from resiliparse.parse.html import HTMLTree
from resiliparse.extract.html2text import extract_plain_text


class ResiliparsePlainExtract(BaseExtractor):

    name = 'resiliparse-plain'

    @staticmethod
    def extract(html):
        try:
            tree = HTMLTree.parse(html)
            article = extract_plain_text(tree, list_bullets=False, alt_texts=False)
            res = article

        except Exception as e:
            return ''
        return res
