import scrapy
import os.path


class QuoteSpider(scrapy.Spider):
    """ spider to crawl and get the required data """
    name = "quotes"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = os.path.join(
            "C:\\myprojects\\sc_tuts\\tutorial\\tmp", f'quotes-{page}.html')
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log("scraping is done")
