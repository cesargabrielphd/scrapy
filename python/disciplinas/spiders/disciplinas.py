import scrapy
from scrapy.http import FormRequest

class DisciplinasSpider(scrapy.Spider):
    name = 'disciplinas'
    start_urls = [
        "https://sigaa.unb.br/sigaa/public/componentes/busca_componentes.jsf?aba=p-ensino"
    ]

    def parse(self, response):
        # Preencher e enviar o formulário
        return FormRequest.from_response(
            response,
            formdata={
                "form:nivel": "G",  # Exemplo: Graduação
                "form:tipo": "2",  # Exemplo: Disciplina
                "form:checkCodigo": "",  # Desmarcado
                "form:j_id_jsp_190531263_11": "",  # Código vazio
                "form:checkNome": "",  # Desmarcado
                "form:j_id_jsp_190531263_13": "",  # Nome vazio
                "form:checkUnidade": "",  # Desmarcado
                "form:unidades": "518"  # Unidade acadêmica não selecionada
            },
            callback=self.after_form_submission
        )

    def after_form_submission(self, response):
        # Processar a resposta após o envio do formulário
        # ...existing code...
        pass
        # ...existing code...
