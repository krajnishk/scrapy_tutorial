# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoteItem(scrapy.Item):
    """ Storing fields for Quote"""
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()


class AuthorItem(scrapy.Item):
    """ Storing fields for Author"""
    # define the fields for your item here like:
    author_name = scrapy.Field()
    author_dob = scrapy.Field()
    author_pob = scrapy.Field()
    author_bio = scrapy.Field()


class QuoteTagItem(scrapy.Item):
    """ Storing fields for a specific Tag"""
    # define the fields for your item here like:
    text = scrapy.Field()
    author = scrapy.Field()
