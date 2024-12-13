import os
import scrapy
import json
from scrapy.http import FormRequest


class DisciplinaSpider(scrapy.Spider):
    name = "disciplina"
    allowed_domains = ["sigaa.unb.br"]
    start_urls = [
        "https://sigaa.unb.br/sigaa/public/componentes/busca_componentes.jsf?aba=p-ensino"
    ]
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_URI": "temp.json",  # Temporarily save data to temp.json
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
        # Salva os dados coletados no arquivo temp.json
        temp_file_path = "temp.json"
        disciplinas = []

        # Itera sobre as linhas da tabela
        for linha in response.css("table.listagem tbody tr"):
            codigo = linha.css("td:nth-child(1)::text").get()
            nome = linha.css("td:nth-child(2)::text").get()
            tipo = linha.css("td:nth-child(3)::text").get()
            ch_total = linha.css("td:nth-child(4)::text").get()
            id_componente = linha.css("a[title='Programa Atual do Componente']::attr(onclick)").re(r"idComponente':'(\d+)'")[0]

            disciplina = {
                "Código": codigo,
                "Nome": nome,
                "Tipo": tipo,
                "Carga_Horária": ch_total,
                "ID_Componente": id_componente,  # Adicionando ID da disciplina
            }
            disciplinas.append(disciplina)

            # Gerar o link para acessar a ementa
            ementa_url = f"https://sigaa.unb.br/sigaa/public/componentes/ementa_componentes.jsf?idComponente={id_componente}"
            # Fazer a requisição para baixar o PDF
            yield scrapy.Request(ementa_url, callback=self.download_pdf, meta={'codigo': codigo, 'nome': nome})

        # Grava os dados em temp.json
        with open(temp_file_path, "w", encoding="utf-8") as temp_file:
            json.dump(disciplinas, temp_file, ensure_ascii=False, indent=4)

        # Remover o arquivo temp.json após a operação
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    def download_pdf(self, response):
        # Cria a pasta GRADMAT se não existir
        folder = "GRADMAT"
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Nome do arquivo com base no código e nome da disciplina
        codigo = response.meta['codigo']
        nome = response.meta['nome']
        pdf_filename = f"{folder}/{codigo}_{nome}.pdf"

        # Baixa o PDF
        with open(pdf_filename, 'wb') as f:
            f.write(response.body)

        self.log(f"PDF da disciplina {nome} ({codigo}) salvo como {pdf_filename}")
