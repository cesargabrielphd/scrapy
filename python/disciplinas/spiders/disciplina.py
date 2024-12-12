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
            "form": "form",
            "form:nivel": "G",  # GRADUAÇÃO
            "form:checkTipo": "on",  # Selecionar Tipo do Componente
            "form:tipo": "2",  # DISCIPLINA
            "form:checkCodigo": "",
            "form:j_id_jsp_190531263_11": "",  # Código do componente vazio
            "form:checkNome": "",
            "form:j_id_jsp_190531263_13": "",  # Nome do componente vazio
            "form:checkUnidade": "on",  # Selecionar Unidade Responsável
            "form:unidades": "518",  # DEPARTAMENTO DE MATEMÁTICA - BRASÍLIA - 11.01.01.15.03
            "javax.faces.ViewState": view_state,  # ViewState necessário para envio
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