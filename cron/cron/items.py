# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapItem(scrapy.Item):
    headline = scrapy.Field()
    article_link = scrapy.Field()
    date = scrapy.Field()
    detail = scrapy.Field()
    source_site = scrapy.Field()
    created_at = scrapy.Field()

class PressReleaseItem(scrapy.Item):
    headline = scrapy.Field()
    article_link = scrapy.Field()
    date = scrapy.Field()
    release_no = scrapy.Field()

class PublicStatementItem(scrapy.Item):
    title = scrapy.Field()
    article_link = scrapy.Field()
    speaker = scrapy.Field()
    date = scrapy.Field()
