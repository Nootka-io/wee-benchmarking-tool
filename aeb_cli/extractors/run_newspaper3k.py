from newspaper import Article
from extractors import BaseExtractor


class Newspaper3kExtract(BaseExtractor):

    name = 'newspaper3k'

    @staticmethod
    def extract(html):
        try:
            article = Article('https://example.com')
            article.set_html(html)
            article.parse()
            res = article.text
        except:
            return ''
        return res
