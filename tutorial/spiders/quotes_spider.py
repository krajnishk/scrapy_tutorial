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


class AuthorSpider(scrapy.Spider):
    """ Spider to get the author details """
    name = "author"

    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):
        """ Parse the page to extarct the author link """

        author_page_urls = response.xpath(
            "//span/a[contains(@href, 'author')]/@href")
        yield from response.follow_all(author_page_urls, self.parse_author)

        pagination_urls = response.xpath('//li[@class="next"]/a/@href')
        yield from response.follow_all(pagination_urls, self.parse)

    def parse_author(self, response):
        """ Parse author page to get the data """
        yield {
            'author_name':   response.xpath(".//h3[@class='author-title']/text()").get().strip(),
            'author_dob':   response.xpath(".//span[@class='author-born-date']/text()").get().strip(),
            'author_pob':   response.xpath(".//span[@class='author-born-location']/text()").get().strip('in '),
            'author_bio':   response.xpath(".//div[@class='author-description']/text()").get().strip()
        }
