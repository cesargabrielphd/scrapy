import scrapy
from scrapy.http import Request
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.selector import Selector


class PlantsSpider(scrapy.Spider):
    name = "plants"
    allowed_domains = ["sigaa.unb.br"]
    start_urls = [
        "https://sigaa.unb.br/sigaa/public/componentes/busca_componentes.jsf?aba=p-ensino"
    ]

    custom_settings = {"ROBOTSTXT_OBEY": False}  # Desativa a obediência ao robots.txt

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.open_with_selenium)

    def open_with_selenium(self, response):
        # Configura o Selenium WebDriver
        self.log("Abrindo o navegador para preenchimento manual do formulário...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(response.url)

        # Espera 2 minutos para preenchimento manual do formulário
        self.log("Esperando 2 minutos para preenchimento manual do formulário...")

        time.sleep(30)

        # Obtém o HTML da página após o preenchimento manual
        html = driver.page_source
        driver.quit()

        # Continua o scraping com Scrapy
        sel = Selector(text=html)
        departamento_option = sel.css(
            "select#form\\:unidades option[value='518']::text"
        ).get()
        if departamento_option and (
            departamento_option.startswith("DEPTO")
            or departamento_option.startswith("DEPARTAMENTO")
        ):
            departamento_nome = departamento_option.split(" - ")[0]
        else:
            departamento_nome = "Desconhecido"

        yield Request(
            url=response.url,
            callback=self.after_form_submission,
            meta={"departamento_nome": departamento_nome, "disciplinas": []},
            dont_filter=True,
        )

    def after_form_submission(self, response):
        # ...existing code...
        departamento_nome = response.meta["departamento_nome"]
        disciplinas = response.meta["disciplinas"]
        rows = response.css("tr.linhaPar, tr.linhaImpar")
        self.log(f"Encontradas {len(rows)} disciplinas na página atual.")
        for row in rows:
            codigo = row.css("td:nth-child(1)::text").get()
            if codigo and codigo.startswith(
                "MAT"
            ):  # Filtra apenas disciplinas de matemática
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
