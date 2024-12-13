import scrapy
import json
from scrapy.http import FormRequest
import os
import time


class RecursividadeSpider(scrapy.Spider):
    name = "recursividade"
    allowed_domains = ["sigaa.unb.br"]
    start_urls = [
        "https://sigaa.unb.br/sigaa/public/componentes/busca_componentes.jsf?aba=p-ensino"
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Carrega o arquivo de opções do formulário
        with open("../../opcoes_formulario.json", "r", encoding="utf-8") as f:
            self.form_options = json.load(f)

        # Filtra todos os departamentos e garante que captura "DEPARTAMENTO" e "DEPTO"
        self.departamentos = [
            item
            for item in self.form_options["unidades"]
            if "DEPARTAMENTO" in item["text"].upper() or "DEPTO" in item["text"].upper()
        ]

        # Contador para as páginas processadas
        self.pagina_count = 0

    def parse(self, response):
        # Captura o estado do formulário (ViewState)
        view_state = response.css(
            'input[name="javax.faces.ViewState"]::attr(value)'
        ).get()

        for departamento in self.departamentos:
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
                "form:unidades": departamento["value"],  # Unidade do departamento
                "javax.faces.ViewState": view_state,  # ViewState necessário para envio
            }

            # Envia uma requisição para cada departamento
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.after_form_submission,
                meta={
                    "departamento": departamento["text"]
                },  # Passa o nome do departamento para o callback
            )

    def after_form_submission(self, response):
        departamento_nome = response.meta["departamento"]
        disciplinas = []

        # Itera sobre as linhas da tabela
        for linha in response.css("table.listagem tbody tr"):
            codigo = linha.css("td:nth-child(1)::text").get()
            nome = linha.css("td:nth-child(2)::text").get()
            tipo = linha.css("td:nth-child(3)::text").get()
            ch_total = linha.css("td:nth-child(4)::text").get()

            disciplina = {
                "Código": codigo,
                "Nome": nome,
                "Tipo": tipo,
                "Carga_Horária": ch_total,
            }
            disciplinas.append(disciplina)

        # Salva os dados do departamento no arquivo local
        if not os.path.exists("departamentos"):
            os.makedirs("departamentos")

        departamento_file = os.path.join("departamentos", f"{departamento_nome}.json")
        with open(departamento_file, "w", encoding="utf-8") as file:
            json.dump(disciplinas, file, ensure_ascii=False, indent=4)

        self.log(
            f"Dados do departamento {departamento_nome} salvos em {departamento_file}"
        )

        # A cada 10 páginas, aguarda antes de continuar
        self.pagina_count += 1
        if self.pagina_count % 10 == 0:
            self.log(
                f"Aguardando 5 segundos após {self.pagina_count} páginas processadas..."
            )
            time.sleep(5)  # Atraso de 5 segundos

        # Verificar se há mais páginas para recursão
        proxima_pagina = response.css('a[title="Próxima"]::attr(href)').get()
        if proxima_pagina:
            yield response.follow(proxima_pagina, callback=self.after_form_submission)
