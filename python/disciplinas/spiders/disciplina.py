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

            disciplina = {
                "Código": codigo,
                "Nome": nome,
                "Tipo": tipo,
                "Carga_Horária": ch_total,
            }
            disciplinas.append(disciplina)

        # Grava os dados em temp.json
        with open(temp_file_path, "w", encoding="utf-8") as temp_file:
            json.dump(disciplinas, temp_file, ensure_ascii=False, indent=4)

        # Verifica se o arquivo disciplinas.json existe
        if os.path.exists("disciplinas.json"):
            # Lê os dados do arquivo disciplinas.json
            with open("disciplinas.json", "r", encoding="utf-8") as json_file:
                existing_disciplinas = json.load(json_file)

            # Compara as disciplinas dos dois arquivos
            with open(temp_file_path, "r", encoding="utf-8") as temp_file:
                temp_disciplinas = json.load(temp_file)

            # Se os dados forem diferentes, atualize o disciplinas.json
            if existing_disciplinas != temp_disciplinas:
                with open("disciplinas.json", "w", encoding="utf-8") as json_file:
                    json.dump(temp_disciplinas, json_file, ensure_ascii=False, indent=4)

        else:
            # Se disciplinas.json não existe, cria o arquivo com os dados do arquivo temporário
            with open("disciplinas.json", "w", encoding="utf-8") as json_file:
                with open(temp_file_path, "r", encoding="utf-8") as temp_file:
                    temp_disciplinas = json.load(temp_file)
                    json.dump(temp_disciplinas, json_file, ensure_ascii=False, indent=4)

        # Remover o arquivo temp.json após a operação
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
