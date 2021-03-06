import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from datetime import datetime

from cron.items import ScrapItem


class SecRulesSroNysearcaCboebzxSpider(Spider):
    name = "sec_rules_sro_nysearca_cboebzx"
    allowed_domains = ["www.sec.gov"]
    start_urls = [
        'https://www.sec.gov/rules/sro/nysearca.htm',
        'https://www.sec.gov/rules/sro/cboebzx.htm'
    ]

    items = []

    def parse(self, response):
        scrapItems = response.xpath('//table/tbody/tr')
       
        i = 2
        while i<len(scrapItems):
            item = ScrapItem()
            
            tds = scrapItems[i].xpath('td')
            item['headline'] = tds[2].xpath('b[@class="blue"]/text()').extract()[0]
            item['article_link'] = 'https://www.sec.gov' + tds[0].xpath('a/@href').extract()[0]
            
            datetime_str = tds[1].xpath('text()').extract()[0]
            item['date'] = item['date'] = datetime.strptime(datetime_str, '%b. %d, %Y').strftime('%Y-%m-%d')

            item['source_site'] = self.start_urls[0]
            item['created_at'] = datetime.today().strftime('%Y-%m-%d')
            yield item
            i+=2
