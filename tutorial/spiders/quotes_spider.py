import scrapy


class QuoteSpider(scrapy.Spider):
    """ spider to crawl and get the required data """
    name = "quotes"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        """ Parse the html page to extract the data """
        for quote in response.xpath("//div[@class='quote']"):
            yield {
                'text': quote.xpath(".//span[@class='text']/text()").get(),
                'author': quote.xpath(".//small[@class='author']/text()").get(),
                'tags': quote.xpath(".//div[@class = 'tags']/a[@class='tag']/text()").getall()
            }

        #   Pagination, handling next pages
        next_page_url = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)
