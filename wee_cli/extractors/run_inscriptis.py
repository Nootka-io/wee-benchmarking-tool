from inscriptis import get_text
from wee_cli.extractors import BaseExtractor

class InscriptisExtract(BaseExtractor):

    name = 'inscriptis'

    @staticmethod
    def extract(html):
        try:
            content = get_text(html)
            res = content
        except:
            return ''
        return res
