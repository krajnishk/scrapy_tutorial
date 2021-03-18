import scrapy


class QuoteArgSpider(scrapy.Spider):
    """ Spider class to crawl based on argument """
    name = "quote_arg"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """ Parse the tag html page to extract the data """
        for quote in response.xpath("//div[@class='quote']"):
            yield {
                'text': quote.xpath(".//span[@class='text']/text()").get(),
                'author': quote.xpath(".//small[@class='author']/text()").get(),
            }

        #   Pagination, handling next pages
        next_page_url = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)
