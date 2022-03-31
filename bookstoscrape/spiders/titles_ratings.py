import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# let's try to use CrawlSpider.
class TitlesRatingsSpider(CrawlSpider):
    name = 'titles_ratings'
    allowed_domains = ['books.toscrape.com']

    # Disguise User Agent as something organic, like my real browser user agent
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"

    # Override the User-Agent in header of starting requests.
    def start_requests(self):
        yield scrapy.Request(url="http://books.toscrape.com/", headers={
            'User-Agent': self.user_agent
        })


    rules = (
        # Open each book link 
        Rule(LinkExtractor(restrict_xpaths="//ol[@class='row']/li"), callback='parse_item', follow=True),
        
        # Link to next page
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"), process_request="set_user_agent"),
    )

    # Does the same thing as start_requests() but for subsequent requests.
    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request


    def parse_item(self, response):
        book_title = response.xpath("//h1/text()").get()
        book_price = response.xpath("//p[@class='price_color']/text()").get()

        yield {
            "title": book_title,
            "price": book_price,
            "user-agent": response.request.headers['User-Agent'].decode('utf-8') # Just to verify the spoofing is happening
        }
