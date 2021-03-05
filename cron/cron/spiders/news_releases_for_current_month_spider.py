import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from datetime import datetime

from cron.items import ScrapItem


class NewsReleasesForCurrentMonthSpider(Spider):
    name = "newsreleasesforcurrentmonth"
    allowed_domains = ["www.irs.gov"]
    start_urls = [
        'https://www.irs.gov/newsroom/news-releases-for-current-month'
    ]

    items = []

    def parse(self, response):
        scrapItems = response.xpath('//div[@class="media"]')

        for scrapItem in scrapItems:
            item = ScrapItem()
            item['headline'] = scrapItem.xpath('h3/a/text()').extract()[0].strip()
            item['article_link'] = 'https://www.irs.gov' + scrapItem.xpath('h3/a/@href').extract()[0]

            description = scrapItem.xpath('div/text()').extract()[0].split(" ")
            date = description[1] + " "+ description[2] + description[3]

            try:
                item['date'] = datetime.strptime(date, '%B %d,%Y').strftime('%Y-%m-%d')
            except:
                item['date'] = datetime.today().strftime('%Y-%m-%d')

            item['source_site'] = self.start_urls[0]
            item['created_at'] = datetime.today().strftime('%Y-%m-%d')

            self.items.append(item)
            yield scrapy.Request(item['article_link'], callback = self.parse_dir_contents)


    def parse_dir_contents(self, response):
        detail = response.xpath("//article[@role='article']/div[@class='col-md-12 col-sm-12 col-xs-12']/div[@class='field field--name-body field--type-text-with-summary field--label-hidden field--item']").extract()[0]
       
        for item in self.items:
            if item['article_link'] == response.url:
                item['detail'] = detail
                yield item
       