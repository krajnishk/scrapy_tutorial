import scrapy
from .. items import QuoteTagItem

# Not working all the time.. need to revisit the parse function
# Redirect : 308 to be handled


class QuotesSpider(scrapy.Spider):
    name = "quotetag"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        """ Parse the quotes with specific dags """

        items = QuoteTagItem()

        for quote in response.css('div.quote'):
            text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            items['text'] = text
            items['author'] = author

            yield items

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
