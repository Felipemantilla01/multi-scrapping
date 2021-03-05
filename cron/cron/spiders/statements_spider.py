import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from datetime import datetime

from cron.items import ScrapItem


class PublicStatementsSpider(Spider):
    name = "publicstatements"
    allowed_domains = ["www.sec.gov"]
    start_urls = [
        'https://www.sec.gov/news/statements'
    ]

    items = []
    
    def parse(self, response):
        scrapItems = response.xpath('//tr[@class="ps-list-page-row"]')

        for scrapItem in scrapItems:
            item = ScrapItem()
            item['headline'] = scrapItem.xpath('td[@headers="view-field-display-title-table-column"]/a/text()').extract()[0]
            item['article_link'] = 'https://www.sec.gov' + scrapItem.xpath('td[@headers="view-field-display-title-table-column"]/a/@href').extract()[0]
            datetime_str = scrapItem.xpath('td[@headers="view-field-publish-date-table-column"]/time/text()').extract()[0]
            datetime_str = datetime_str.replace('April', 'Apr')
            datetime_str = datetime_str.replace('March', 'Mar')
            datetime_str = datetime_str.replace('June', 'Jun')
            datetime_str = datetime_str.replace('July', 'Jul')
            datetime_str = datetime_str.replace('Sept', 'Sep')
            
            try:
                item['date'] = datetime.strptime(datetime_str, '%b. %d, %Y').strftime('%Y-%m-%d')
            except:
                item['date'] = datetime.strptime(datetime_str, '%b %d, %Y').strftime('%Y-%m-%d')

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