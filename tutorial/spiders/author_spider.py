import scrapy


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
