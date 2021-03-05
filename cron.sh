#!/bin/bash
echo "cron job started" >> /var/log/cron.log 2>&1

PATH=$PATH:/usr/local/bin
export PATH

cd /app/cron/cron
scrapy crawl pressreleases >> /var/log/cron.log 2>&1
scrapy crawl publicstatements >> /var/log/cron.log 2>&1

scrapy crawl browse_edgar >> /var/log/cron.log 2>&1
scrapy crawl cnbc >> /var/log/cron.log 2>&1
scrapy crawl pressroom_pressreleases >> /var/log/cron.log 2>&1

scrapy crawl newsreleasesforcurrentmonth >> /var/log/cron.log 2>&1
scrapy crawl speesches_testimony >> /var/log/cron.log 2>&1

