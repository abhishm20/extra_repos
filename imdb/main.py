import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from imdbyear.items import MovieItem

class IMDBSpider(CrawlSpider):
    name = 'imdb'
    rules = (
        # extract links at the bottom of the page. note that there are 'Prev' and 'Next'
        # links, so a bit of additional filtering is needed
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="right"]/span/a')),
            process_links=lambda links: filter(lambda l: 'Next' in l.text, links),
            callback='parse_page',
            follow=True),
    )

    def __init__(self, start=None, end=None, *args, **kwargs):
      super(IMDBSpider, self).__init__(*args, **kwargs)
      self.start_year = int(start) if start else 1874
      self.end_year = int(end) if end else 2016

    # generate start_urls dynamically
    def start_requests(self):
        for year in range(self.start_year, self.end_year+1):
            yield scrapy.Request('http://www.imdb.com/search/title?year=%d,%d&title_type=feature&sort=moviemeter,asc' % (year, year))

    def parse_page(self, response):
        for sel in response.xpath("//*[@class='results']/tr/td[3]"):
            item = MovieItem()
            item['Title'] = sel.xpath('a/text()').extract()[0]
            # note -- you had 'MianPageUrl' as your scrapy field name. I would recommend fixing this typo
            # (you will need to change it in items.py as well)
            item['MainPageUrl']= "http://imdb.com"+sel.xpath('a/@href').extract()[0]
            request = scrapy.Request(item['MainPageUrl'], callback=self.parseMovieDetails)
            request.meta['item'] = item
            yield request
    # make sure that the dynamically generated start_urls are parsed as well
    parse_start_url = parse_page

    # do your magic
    def parseMovieDetails(self, response):
        print response