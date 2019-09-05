# -*- coding: utf-8 -*-

# Scrapy settings for befrank project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'befrank'

SPIDER_MODULES = ['befrank.spiders']
NEWSPIDER_MODULE = 'befrank.spiders'

DOWNLOAD_DELAY = 5
CONCURRENT_REQUESTS = 250

ITEM_PIPELINES = {
    'befrank.pipelines.BefrankPipeline': 0
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tutorial (+http://www.yourdomain.com)'
