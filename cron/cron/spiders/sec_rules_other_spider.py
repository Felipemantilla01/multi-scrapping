import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from datetime import datetime

from cron.items import ScrapItem


class SecRulesOtherSpider(Spider):
    name = "sec_rules_other"
    allowed_domains = ["www.sec.gov"]
    start_urls = [
        'https://www.sec.gov/rules/other.htm'
    ]

    items = []

    def parse(self, response):
        scrapItems = response.xpath('//table[@id="mainlist"]/tbody/tr')
        print(scrapItems)
        
        for scrapItem in scrapItems:
            item = ScrapItem()
            try:
                if scrapItem.xpath("@id").extract()[0] == 'firstq':
                    continue
            except:
                tds = scrapItem.xpath('td')
                item['headline'] = tds[2].xpath('b[@class="blue"]/text()').extract()[0]
                item['article_link'] = 'https://www.sec.gov' + tds[0].xpath('a/@href').extract()[0]
                
                datetime_str = tds[1].xpath('text()').extract()[0]
                item['date'] = item['date'] = datetime.strptime(datetime_str, '%b. %d, %Y').strftime('%Y-%m-%d')

                item['source_site'] = self.start_urls[0]
                item['created_at'] = datetime.today().strftime('%Y-%m-%d')

                yield item