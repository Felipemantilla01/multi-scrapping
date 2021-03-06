import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from datetime import datetime

from cron.items import ScrapItem


class SecNewsSpeechesSpider(Spider):
    name = "sec_news_speeches"
    allowed_domains = ["www.sec.gov"]
    start_urls = [
        'https://www.sec.gov/news/speeches'
    ]

    items = []

    def parse(self, response):
        scrapItems = response.xpath('//table/tbody/tr[contains(@class, "speeches-list-row")]')
        
        for scrapItem in scrapItems:
            item = ScrapItem()

            item['headline'] = scrapItem.xpath('td[@headers="view-field-display-title-table-column"]/a/text()').extract()[0]
            item['article_link'] = 'https://www.sec.gov' + scrapItem.xpath('td[@headers="view-field-display-title-table-column"]/a/@href').extract()[0]
            
            datetime_str = scrapItem.xpath('td[@headers="view-field-publish-date-table-column"]/time/@datetime').extract()[0]
            item['date'] = datetime_str

            item['source_site'] = self.start_urls[0]
            item['created_at'] = datetime.today().strftime('%Y-%m-%d')

            self.items.append(item)
            yield scrapy.Request(item['article_link'], callback = self.parse_dir_contents)

    def parse_dir_contents(self, response):
        detail = response.xpath("//article[@role='article']").extract()[0]
       
        for item in self.items:
            if item['article_link'] == response.url:
                item['detail'] = detail
                yield item