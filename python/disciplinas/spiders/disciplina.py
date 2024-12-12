import scrapy
from scrapy.http import FormRequest

class DisciplinasSpider(scrapy.Spider):
    name = "disciplinas"
    allowed_domains = ["sigaa.unb.br"]
    start_urls = [
        "https://sigaa.unb.br/sigaa/public/componentes/busca_componentes.jsf?aba=p-ensino"
    ]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'disciplinas.json'
    }

    def parse(self, response):
        formdata = {
            "form:nivel": "G",
            "form:tipo": "2",
            "form:checkTipo": "on",
            "form:j_id_jsp_190531263_11": "MAT0311",
            "form:checkCodigo": "on",
            "form:j_id_jsp_190531263_13": "Matemática",
            "form:checkNome": "on",
            "form:unidades": "518",
            "form:checkUnidade": "on",
            "javax.faces.ViewState": response.css('input[name="javax.faces.ViewState"]::attr(value)').get()
        }

        return FormRequest.from_response(
            response, formdata=formdata, callback=self.after_form_submission
        )

    def after_form_submission(self, response):
        for linha in response.css("table.listagem tbody tr"):
            yield {
                "codigo": linha.css("td:nth-child(1)::text").get(),
                "nome": linha.css("td:nth-child(2)::text").get(),
                "tipo": linha.css("td:nth-child(3)::text").get(),
                "ch_total": linha.css("td:nth-child(4)::text").get(),
            }
