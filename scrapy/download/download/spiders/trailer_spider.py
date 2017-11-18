
import scrapy


class TrailerSpider(scrapy.Spider):
    name = "trailer"

    #        start_urls = ["https://www.themoviedb.org/movie/upcoming/"]
    # start_urls = ['http://www.allocine.fr/film/agenda/sem-2017-09-27/','http://www.allocine.fr/film/agenda/sem-2017-09-20/','http://www.allocine.fr/film/agenda/sem-2017-09-13/']
    start_urls = ['http://www.allocine.fr/film/sorties-semaine/']

    def parse(self, response):
        for quote in response.css('div.card.card-entity.card-entity-list.cf.hred'):
            yield {
                'titre': quote.css('.meta-title a::text').extract_first(),
                'genre': quote.css('div.meta-body-item.meta-body-info span::text').extract(),
                'trailer': quote.css('div.meta-more a::attr(href)').extract_first(),
                'synopsis': quote.css('div.synopsis::text').extract_first()
            }
