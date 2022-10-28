from wee_cli.extractors import BaseExtractor
from trafilatura import extract


class TrafilaturaExtract(BaseExtractor):

    name = 'trafilatura'

    @staticmethod
    def extract(html):
        try:
            res = extract(html)
        except:
            return ''
        return res
