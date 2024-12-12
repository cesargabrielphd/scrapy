import os
import scrapy
from scrapy.http import FormRequest
import pdfkit


class DisciplinasSpider(scrapy.Spider):
    name = "disciplinas"
    allowed_domains = ["sigaa.unb.br"]
    start_urls = [
        "https://sigaa.unb.br/sigaa/public/componentes/busca_componentes.jsf?aba=p-ensino"
    ]
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_URI": "disciplinas.json",
    }

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
        # Nome do departamento (usado para criar a pasta)
        departamento = "DEPARTAMENTO_DE_MATEMATICA"
        if not os.path.exists(departamento):
            os.makedirs(departamento)

        # Itera sobre as linhas da tabela
        for linha in response.css("table.listagem tbody tr"):
            codigo = linha.css("td:nth-child(1)::text").get()
            nome = linha.css("td:nth-child(2)::text").get()
            tipo = linha.css("td:nth-child(3)::text").get()
            ch_total = linha.css("td:nth-child(4)::text").get()

            # ID da disciplina para acessar a ementa
            id_componente = linha.css(
                'a[title="Programa Atual do Componente"]::attr(onclick)'
            )
            id_componente = self.extract_id_from_onclick(id_componente.get())

            yield {
                "codigo": codigo,
                "nome": nome,
                "tipo": tipo,
                "ch_total": ch_total,
            }

            # Gera URL para acessar a ementa
            if id_componente:
                ementa_url = "https://sigaa.unb.br/sigaa/public/componentes/busca_componentes.jsf"
                formdata = {
                    "formListagemComponentes:j_id_jsp_190531263_27j_id_109": "formListagemComponentes:j_id_jsp_190531263_27j_id_109",
                    "idComponente": id_componente,
                    "javax.faces.ViewState": response.css(
                        'input[name="javax.faces.ViewState"]::attr(value)'
                    ).get(),
                }

                # Faz o download da página de ementa
                yield FormRequest(
                    url=ementa_url,
                    formdata=formdata,
                    callback=self.save_ementa,
                    meta={"codigo": codigo, "nome": nome, "departamento": departamento},
                )

    def extract_id_from_onclick(self, onclick_text):
        """Extrai o idComponente do atributo onclick."""
        try:
            id_componente = onclick_text.split("idComponente':'")[1].split("'}")[0]
            return id_componente
        except IndexError:
            return None

    def save_ementa(self, response):
        # Dados da disciplina
        codigo = response.meta["codigo"]
        nome = response.meta["nome"]
        departamento = response.meta["departamento"]

        # Criar arquivos HTML e PDF
        html_filename = os.path.join(departamento, f"{codigo}_{nome}.html")
        pdf_filename = os.path.join(departamento, f"{codigo}_{nome}.pdf")

        # Salvar HTML
        with open(html_filename, "w", encoding="utf-8") as f:
            f.write(response.text)

        # Converter para PDF
        try:
            pdfkit.from_file(html_filename, pdf_filename)
        except Exception as e:
            self.logger.error(f"Erro ao gerar PDF para {codigo} - {nome}: {e}")
