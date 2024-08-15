from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

from itemloaders.processors import MapCompose

class Articulo(Item):
    id = Field()
    titulo = Field()
    precio = Field()
    descripcion = Field()

class MercadoLibreCrawler(CrawlSpider):
    name = 'mercadoLibre'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 50
    }

    download_delay = 3

    allowed_domains = ['listado.mercadolibre.com.ec', 'articulo.mercadolibre.com.ec']

    start_urls = ['https://listado.mercadolibre.com.ec/cachorros-golden-retriever']

    rules = (
        # Paginacion
        Rule(
            LinkExtractor(
                allow=r'_Desde_\d+'
            ), follow=True
        ),
        # Detalle articulos
        Rule(
            LinkExtractor(
                allow=r'/MEC-'
            ), follow=True, callback="parse_articulo"
        ),
    )

    def quitarDolar(self, texto):
        return texto.replace("$", "")

    def parse_articulo(self, response):
        item = ItemLoader(Articulo(), response)
        item.add_xpath('titulo', '//h1[@class="ui-pdp-title"]/text()')
        item.add_xpath('precio', '//span[@class="andes-money-amount__fraction"]/text()')
        item.add_xpath('descripcion', '//p[@class="ui-pdp-description__content"]/text()')

        yield item.load_item()