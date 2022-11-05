import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news_scraper.items import NewsArticle

class CnnPySpider(scrapy.Spider):
    name = 'cnn.py'
    allowed_domains = ['edition.cnn.com']
    start_urls = ['https://edition.cnn.com/africa']

    rules = [Rule(LinkExtractor(allow=r'\/2020\/[0-9][0-9]\/[0-9][0-9]\/[a-zA-Z\-]+\/[a-zA-Z\-]+\/index.html'), callback='parse_item', follow=True)]
    
    def parse_item(self, response):
        article = NewsArticle()
        # <script data-rh="true">
        article['url'] = response.url
        article['source'] = 'CNN'
        article['title'] = response.xpath('//h1/text()').get()
        article['description'] = response.xpath('//meta[@name="description"]/@content').get()
        article['date'] = response.xpath('//meta[@itemprop="datePublished"]/@content').get()
        article['author'] = response.xpath('//meta[@itemprop="author"]/@content').get().replace(', CNN', '')
        article['text'] = response.xpath('//section[@data-zone-label="bodyText"]/div[@class="l-container"]//*/text()').getall()
        return article
