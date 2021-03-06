import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from datetime import datetime

from cron.items import ScrapItem


class FincenNewsRoomSpeechesSpider(Spider):
    name = "fincen_news_rooms_speeches"
    allowed_domains = ["www.fincen.gov"]
    start_urls = [
        'https://www.fincen.gov/news-room/speeches'
    ]

    items = []

    def parse(self, response):

        scrapItems = response.xpath('//div[contains(@class, "views-row")]')
        
        for scrapItem in scrapItems:
            item = ScrapItem()
            item['headline'] = scrapItem.xpath('div[@class="views-field views-field-title"]/span[@class="field-content"]/a/text()').extract()[0]
            item['article_link'] = 'https://www.fincen.gov' + scrapItem.xpath('div[@class="views-field views-field-title"]/span[@class="field-content"]/a/@href').extract()[0]
            datetime_str = scrapItem.xpath('span[@class="views-field views-field-field-date-release"]/span[@class="field-content"]/text()').extract()[0]
            item['date'] = datetime.strptime(datetime_str, '%m/%d/%Y').strftime('%Y-%m-%d')

            item['source_site'] = self.start_urls[0]
            item['created_at'] = datetime.today().strftime('%Y-%m-%d')

            self.items.append(item)
            yield scrapy.Request(item['article_link'], callback = self.parse_dir_contents)

    def parse_dir_contents(self, response):
        detail = response.xpath("//article").extract()[0]
       
        for item in self.items:
            if item['article_link'] == response.url:
                item['detail'] = detail
                yield item
       