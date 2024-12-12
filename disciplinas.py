import scrapy

class DisciplinasSpider(scrapy.Spider):
    name = "disciplinas"
    start_urls = [
        'http://example.com',  # Substitua pela URL inicial desejada
    ]

    def parse(self, response):
        # Seu código de parsing aqui
        pass

# ...existing code...