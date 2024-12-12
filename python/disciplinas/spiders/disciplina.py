import scrapy
from scrapy.http import FormRequest

class DisciplinasSpider(scrapy.Spider):
    name = "disciplinas"
    allowed_domains = ["sigaa.unb.br"]
    start_urls = [
        "https://sigaa.unb.br/sigaa/public/componentes/busca_componentes.jsf?aba=p-ensino"
    ]

    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "disciplinas.json"}

    def parse(self, response):
        # Captura o estado do formulário (ViewState)
        view_state = response.css(
            'input[name="javax.faces.ViewState"]::attr(value)'
        ).get()
        formdata = {
            "formListagemComponentes": "formListagemComponentes",  # Nome do formulário
            "formListagemComponentes:j_id_jsp_190531263_13": "DEPARTAMENTO DE MATEMÁTICA - BRASÍLIA - 11.01.01.15.03",  # Nome da disciplina
            "formListagemComponentes:j_id_jsp_190531263_15": "GRADUAÇÃO",  # Nível
            "formListagemComponentes:j_id_jsp_190531263_17": "DISCIPLINA",  # Tipo
            "javax.faces.ViewState": view_state,  # Estado do formulário
        }


        return FormRequest.from_response(
            response, formdata=formdata, callback=self.after_form_submission
        )

    def after_form_submission(self, response):
        # Itera sobre as linhas da tabela
        for linha in response.css("table.listagem tbody tr"):
            yield {
                "codigo": linha.css(
                    "td:nth-child(1)::text"
                ).get(),  # Código da disciplina
                "nome": linha.css("td:nth-child(2)::text").get(),  # Nome da disciplina
                "tipo": linha.css("td:nth-child(3)::text").get(),  # Tipo
                "ch_total": linha.css("td:nth-child(4)::text").get(),  # Carga horária
            }