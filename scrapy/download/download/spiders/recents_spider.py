
import scrapy
import re
import sqlite3


class RecentSpider(scrapy.Spider):
        name = "recents"

#        start_urls = ["https://www.themoviedb.org/movie/upcoming/"]
#         start_urls = ['http://www.allocine.fr/film/sorties-semaine/']
#         start_urls = ['http://www.allocine.fr/film/agenda/sem-2017-10-11/',
#                       'http://www.allocine.fr/film/agenda/sem-2017-11-01/'
#                       ]

        def start_requests(self):
            urls = [
                'http://www.allocine.fr/film/agenda/sem-2017-12-13/',
                'http://www.allocine.fr/film/agenda/sem-2017-12-20/',
                'http://www.allocine.fr/film/agenda/sem-2017-12-27/',
                'http://www.allocine.fr/film/agenda/sem-2018-01-03/',
                'http://www.allocine.fr/film/agenda/sem-2018-01-10/',
                'http://www.allocine.fr/film/agenda/sem-2018-01-17/',
                'http://www.allocine.fr/film/agenda/sem-2018-01-24/',
                'http://www.allocine.fr/film/agenda/sem-2018-01-31/'
                ]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)
        
        def parse(self, response):
            regex = '(.*)cfilm=(?P<cfilm>[0-9]*).html'
            for quote in response.css('div.card.card-entity.card-entity-list.cf'):
                res = re.match(regex, quote.css('h2.meta-title a::attr(href)').extract_first())
                yield {
                        'titre': quote.css('h2.meta-title a::text').extract_first(),
                        'date': quote.css('div.meta-body-item.meta-body-info span::text').extract_first(),
                        'genre': quote.css('div.meta-body-item.meta-body-info span::text').extract()[3:],
                        'dirs': quote.css('div.meta-body-item.meta-body-direction.light span::text').extract(),
                        'actors': quote.css('div.meta-body-item.meta-body-actor.light span::text').extract(),
                        'cfilm': res.groupdict()['cfilm'] if res else '',
                        'rate': quote.css('span.stareval-note::text').extract(),
                        'synopsis': quote.css('div.synopsis::text').extract_first().strip()
                        }
            for href in response.css('h2.meta-title a::attr(href)'):
                yield response.follow(href, callback=self.parse_trailer)

        def parse_trailer(self, response):
            regex = '(.*)cmedia=(?P<cmedia>[0-9]*)&cfilm=(?P<cfilm>[0-9]*).html'
            for href in response.css('a::attr(href)').extract():
                res = re.match(regex, href)
                if href.startswith('/video/player'):
                    yield {
                        'cmedia': res.groupdict()['cmedia'] if res else '',
                        'cfilm': res.groupdict()['cfilm'] if res else ''
                    }
