from urllib.parse import urlparse

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class LinksSpiderSpider(CrawlSpider):
    name = 'links_spider'

    def __init__(self, url=None, *args, **kwargs):
        self.url = url
        self.domain = urlparse(self.url).netloc
        self.allowed_domains = [self.domain]
        self.start_urls = [self.url]
        super().__init__(*args, **kwargs)
        LinksSpiderSpider.rules = [
            Rule(LinkExtractor(unique=True, allow_domains=[f'{self.domain}']), callback='parse_item'),
        ]

    def parse_item(self, response):
        item = {'url': response.url}
        yield item
