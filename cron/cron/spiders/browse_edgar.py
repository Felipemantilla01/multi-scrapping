import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from datetime import datetime

from cron.items import ScrapItem


class BrowseEdgarSpider(Spider):
    name = "browse_edgar"
    allowed_domains = ["www.sec.gov"]
    start_urls = [
        'https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent'
    ]

    def parse(self, response):
        scrapItemsTables = response.xpath('//table')
        scrapItemsRows = scrapItemsTables[6].xpath('tr')
        
        i = 1
        while i<len(scrapItemsRows):
            item = ScrapItem()
            item['headline'] = scrapItemsRows[i].xpath('td/a/text()').extract()[0]
            item['article_link'] = 'https://www.sec.gov' + scrapItemsRows[i].xpath('td/a/@href').extract()[0]
            item['date'] = scrapItemsRows[i+1].xpath('td/text()').extract()[5]
            item['source_site'] = self.start_urls[0]
            item['created_at'] = datetime.today().strftime('%Y-%m-%d')

            i += 2
            yield item