from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

from itemloaders.processors import MapCompose

class Hotel(Item):
    nombre = Field()
    score = Field()
    descripcion = Field()
    amenities = Field()

class TripAdvisor(CrawlSpider):
    name = 'hotelestripadvisor'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    allowed_domains = ['tripadvisor.es']

    start_urls = ['https://www.tripadvisor.es/Hotels-g187432-Cadiz_Costa_de_la_Luz_Andalucia-Hotels.html']

    download_delay = 2

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-'
            ), follow=True, callback="parse_hotel"),
    )

    def quitarDolar(self, texto):
        return texto.replace("$", "")

    def parse_hotel(self, response):
        sel = Selector(response)

        item = ItemLoader(Hotel(), sel)
        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')
        item.add_xpath('score', '//span[@class="kJyXc P"]/text()',
                        MapCompose(self.quitarDolar))
        item.add_xpath('descripcion', '//div[@id="ABOUT_TAB"]//div[@class="fIrGe _T"]//text()',
                       MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))
        item.add_xpath('amenities',
                       '//div[contains(@data-test-target, "amenity_text")]/text()')
        yield item.load_item()