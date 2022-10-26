from wee_cli.extractors import BaseExtractor
from boilerpy3 import extractors


class BoilerPy3Extract(BaseExtractor):

    name = 'boilerpy3'

    @staticmethod
    def extract(html):
        try:
            extractor = extractors.ArticleExtractor()
            doc = extractor.get_doc(html)
            res = doc.content
        except Exception as e:
            breakpoint()
            return ''
        return res
