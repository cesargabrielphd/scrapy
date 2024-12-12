import scrapy
from scrapy.http import FormRequest


class DisciplinasSpider(scrapy.Spider):
    name = "disciplinas"
    start_urls = [
        "https://sigaa.unb.br/sigaa/public/componentes/busca_componentes.jsf?aba=p-ensino"
    ]

    def parse(self, response):
        formdata = {
            "form:nivel": "G",
            "form:tipo": "2",
            "form:j_id_jsp_190531263_11": "MAT0311",
            "form:j_id_jsp_190531263_13": "Matemática",
            "form:unidades": "672",
        }

        return FormRequest.from_response(
            response, formdata=formdata, callback=self.after_form_submission
        )

    def after_form_submission(self, response):
        for disciplina in response.css("div.resultado"):
            yield {
                "nome": disciplina.css("span.nome::text").get(),
                "codigo": disciplina.css("span.codigo::text").get(),
                "unidade": disciplina.css("span.unidade::text").get(),
            }
