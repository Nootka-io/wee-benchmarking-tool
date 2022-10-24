from extractors import BaseExtractor
from trafilatura import bare_extraction


class TrafilaturaExtract(BaseExtractor):

    name = 'trafilatura'

    @staticmethod
    def extract(html):
        try:
            extract = bare_extraction(html)
            res = extract.get('text')
        except:
            return ''
        return res
