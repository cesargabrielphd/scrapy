import scrapy
from scrapy.http import FormRequest
import json
import time


class PlantsSpider(scrapy.Spider):
    name = "plants"
    allowed_domains = ["sigaa.unb.br"]
    start_urls = [
        "https://sigaa.unb.br/sigaa/public/componentes/busca_componentes.jsf?aba=p-ensino"
    ]

    custom_settings = {"ROBOTSTXT_OBEY": False}  # Desativa a obediência ao robots.txt

    def parse(self, response):
        # Extrai o nome do departamento a partir do campo 'form:unidades'
        departamento_option = response.css(
            "select#form\\:unidades option[value='518']::text"
        ).get()
        if departamento_option and (
            departamento_option.startswith("DEPTO")
            or departamento_option.startswith("DEPARTAMENTO")
        ):
            departamento_nome = departamento_option.split(" - ")[0]
        else:
            departamento_nome = "Desconhecido"

        # Espera antes de preencher o formulário
        self.log("Esperando antes de preencher o formulário...")

        return FormRequest.from_response(
            response,
            formdata={
                "form:nivel": "G",  # GRADUAÇÃO
                "form:tipo": "2",  # DISCIPLINA
                "form:unidades": "518",  # DEPARTAMENTO DE MATEMÁTICA - BRASÍLIA - 11.01.01.15.03
            },
            callback=self.after_form_submission,
            meta={
                "departamento_nome": departamento_nome,
                "disciplinas": [],
                "page_number": 1,
            },
        )

    def parse_details(self, response):
        departamento_nome = response.meta["departamento_nome"]
        disciplinas = response.meta["disciplinas"]
        page_number = response.meta["page_number"]
        rows = response.css("tr.linhaPar, tr.linhaImpar")
        self.log(f"Encontradas {len(rows)} disciplinas na página atual.")
        for row in rows:
            codigo = row.css("td:nth-child(1)::text").get()
            if codigo and codigo.startswith("MAT"):
                nome = row.css("td:nth-child(2)::text").get()
                tipo = row.css("td:nth-child(3)::text").get()
                carga_horaria = row.css("td:nth-child(4)::text").get()
                detalhes_link = row.css(
                    "td:nth-child(5) a[title='Detalhes do Componente Curricular']::attr(href)"
                ).get()
                programa_link = row.css(
                    "td:nth-child(5) a[title='Programa Atual do Componente']::attr(href)"
                ).get()
                disciplinas.append(
                    {
                        "codigo": codigo,
                        "nome": nome,
                        "tipo": tipo,
                        "carga_horaria": carga_horaria,
                        "detalhes_link": detalhes_link,
                        "programa_link": programa_link,
                    }
                )

        # Verifica se há uma próxima página
        next_page = response.css("a[title='Próxima página']::attr(href)").get()
        if next_page:
            self.log(f"Seguindo para a próxima página: {next_page}")
            yield response.follow(
                next_page,
                self.after_form_submission,
                meta={
                    "departamento_nome": departamento_nome,
                    "disciplinas": disciplinas,
                    "page_number": page_number + 1,
                },
            )
        else:
            self.log(f"Extração completa. Total de disciplinas: {len(disciplinas)}")
            # Estrutura o JSON com o nome do departamento e as disciplinas
            departamento = {
                "departamento": departamento_nome,
                "disciplinas": disciplinas,
            }

            # Salva as informações em um arquivo JSON
            with open("disciplina.json", "w", encoding="utf-8") as f:
                json.dump(departamento, f, ensure_ascii=False, indent=4)

        # Verifica se o número de disciplinas é muito alto e salva em um arquivo separado
        if len(disciplinas) >= 2000:
            self.log(
                f"Salvando disciplinas em um arquivo separado devido ao alto número de disciplinas."
            )
            with open(
                f"disciplina_page_{page_number}.json", "w", encoding="utf-8"
            ) as f:
                json.dump(disciplinas, f, ensure_ascii=False, indent=4)
            disciplinas.clear()  # Limpa a lista de disciplinas para a próxima página
