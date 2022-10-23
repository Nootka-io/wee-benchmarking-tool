from extractors import BaseExtractor
from newsplease import NewsPlease


class NewspleaseExtract(BaseExtractor):

    name = 'news-please'

    @staticmethod
    def extract(html):
        try:
            extract = NewsPlease.from_html(html, url=None)
            res = extract.maintext
        except:
            return ''
        return res
