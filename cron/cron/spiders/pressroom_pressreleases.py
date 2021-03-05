import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from datetime import datetime

from cron.items import ScrapItem


class PressRoomPressreleasesSpider(Spider):
    name = "pressroom_pressreleases"
    allowed_domains = ["www.cftc.gov"]
    start_urls = [
        'https://www.cftc.gov/PressRoom/PressReleases'
    ]

    items = []

    def parse(self, response):
        scrapItems = response.xpath('//table/tbody/tr')
        
        for scrapItem in scrapItems:
            item = ScrapItem()

            item['headline'] = scrapItem.xpath('td[@headers="view-field-pdf-link-table-column"]/a/text()').extract()[0]
            item['article_link'] = 'https://www.cftc.gov' + scrapItem.xpath('td[@headers="view-field-pdf-link-table-column"]/a/@href').extract()[0]
            
            datetime_str = scrapItem.xpath('td[@headers="view-field-date-table-column"]/time/text()').extract()[0]
            item['date'] = datetime.strptime(datetime_str, '%m/%d/%Y').strftime('%Y-%m-%d')

            item['source_site'] = self.start_urls[0]
            item['created_at'] = datetime.today().strftime('%Y-%m-%d')

            # yield item
            self.items.append(item)
            yield scrapy.Request(item['article_link'], callback = self.parse_dir_contents)

    def parse_dir_contents(self, response):
        detail = response.xpath("//article[@role='article']").extract()[0]
       
        for item in self.items:
            if item['article_link'] == response.url:
                item['detail'] = detail
                yield item