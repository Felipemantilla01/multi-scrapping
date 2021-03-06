import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from datetime import datetime

from cron.items import ScrapItem


class CnbcSpider(Spider):
    name = "cnbc"
    allowed_domains = ["www.cnbc.com"]
    start_urls = [
        'https://www.cnbc.com/'
    ]

    items = []

    def parse(self, response):
        lastestNews = response.xpath('//div[@class="LatestNews-newsFeed"]')
        
        for lastestNew in lastestNews:
            inner = lastestNew.xpath('div[@class="LatestNews-newsFeedInner"]')
            headline = inner.xpath('div[@class="LatestNews-headline"]')
            item = ScrapItem()
            item['headline'] = headline.xpath('a/text()').extract()[0]
            item['article_link'] = headline.xpath('a/@href').extract()[1] if headline.xpath('a/@href').extract()[0] == '/pro/' else headline.xpath('a/@href').extract()[0]
            item['date'] = datetime.today().strftime('%Y-%m-%d')
            item['source_site'] = self.start_urls[0]
            item['created_at'] = datetime.today().strftime('%Y-%m-%d')

            self.items.append(item)
            yield scrapy.Request(item['article_link'], callback = self.parse_dir_contents)

        riverPlusItems = response.xpath('//div[@class="RiverHeadline-headline RiverHeadline-hasThumbnail"]')
        
        for riverPlusItem in riverPlusItems:
            item = ScrapItem()
            item['headline'] = riverPlusItem.xpath('a/text()').extract()[0]
            item['article_link'] = riverPlusItem.xpath('a/@href').extract()[1] if riverPlusItem.xpath('a/@href').extract()[0] == '/pro/' else riverPlusItem.xpath('a/@href').extract()[0]
            item['date'] = datetime.today().strftime('%Y-%m-%d')
            item['source_site'] = self.start_urls[0]
            item['created_at'] = datetime.today().strftime('%Y-%m-%d')
            
            self.items.append(item)
            yield scrapy.Request(item['article_link'], callback = self.parse_dir_contents)

        otherItems = response.xpath('//div[@class="Card-titleContainer"]')
        
        for otherItem in otherItems:
            print(otherItem)
            item = ScrapItem()
            item['headline'] = otherItem.xpath('a[@class="Card-title"]/div/text()').extract()[0]
            item['article_link'] = otherItem.xpath('a[@class="Card-title"]/@href').extract()[0]
            item['date'] = datetime.today().strftime('%Y-%m-%d')
            item['source_site'] = self.start_urls[0]
            item['created_at'] = datetime.today().strftime('%Y-%m-%d')

            # yield item
            self.items.append(item)
            yield scrapy.Request(item['article_link'], callback = self.parse_dir_contents)


        lazyItems = response.xpath('//li[@class="LazyLoaderPlaceholder-gridItem"]')

        for lazyItem in lazyItems:
            item = ScrapItem()
            item['headline'] = lazyItem.xpath('a/text()').extract()[0]
            item['article_link'] = lazyItem.xpath('a/@href').extract()[0]
            item['date'] = datetime.today().strftime('%Y-%m-%d')
            item['source_site'] = self.start_urls[0]
            item['created_at'] = datetime.today().strftime('%Y-%m-%d')
            
            # yield item
            self.items.append(item)
            yield scrapy.Request(item['article_link'], callback = self.parse_dir_contents)

    def parse_dir_contents(self, response):
        details = response.xpath("//div[@class='group']").extract()
       
        for item in self.items:
            if item['article_link'] == response.url:
                item['detail'] = ''
                for detail in details:
                    item['detail'] += detail
                yield item