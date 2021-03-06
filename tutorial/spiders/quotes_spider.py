import scrapy
from .. items import QuoteItem
from scrapy.http import FormRequest


class QuoteSpider(scrapy.Spider):
    """ spider to crawl and get the required data """
    name = "quotes"
    page_no = 2

    start_urls = [
        'http://quotes.toscrape.com/login'
    ]

    def parse(self, response):
        """ Parse the html page to extract the data """

        token = response.xpath(".//input[@name='csrf_token']/@value").get()
        print(token)
        return FormRequest.from_response(response, formdata={
            'csrf_token': token,
            'username': 'abc123',
            'passwd': 'abc123'
        }, callback=self.start_scraping
        )

    def start_scraping(self, response):

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

        next_page_url = 'http://quotes.toscrape.com/page/' + \
            str(QuoteSpider.page_no) + '/'
        # if next_page_url is not None:
        if QuoteSpider.page_no < 4:
            QuoteSpider.page_no += 1
            yield response.follow(next_page_url, callback=self.start_scraping)
