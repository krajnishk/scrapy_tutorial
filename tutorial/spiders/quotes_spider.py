import scrapy
from .. items import QuoteItem


class QuoteSpider(scrapy.Spider):
    """ spider to crawl and get the required data """
    name = "quotes"

    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        """ Parse the html page to extract the data """

        items = QuoteItem()

        for quote in response.xpath("//div[@class='quote']"):
            title = quote.xpath(".//span[@class='text']/text()").get()
            author = quote.xpath(".//small[@class='author']/text()").get()
            tags = quote.xpath(
                ".//div[@class = 'tags']/a[@class='tag']/text()").getall()

            items['title'] = title
            items['author'] = author
            items['tags'] = tags

            yield items

        #   Pagination, handling next pages
        # next_page_url = response.xpath('//li[@class="next"]/a/@href').get()
        # if next_page_url is not None:
        #     yield response.follow(next_page_url, callback=self.parse)
