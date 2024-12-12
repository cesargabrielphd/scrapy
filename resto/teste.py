from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def download_html(url):
    # Configurações do ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa o Chrome em modo headless (sem interface gráfica)
    service = Service('chromedriver.exe')  # Caminho para o chromedriver

    # Inicializa o WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navega até a página desejada
        driver.get(url)

        # Espera um tempo para garantir que a página foi carregada completamente
        time.sleep(2)

        # Verifica se a página foi carregada corretamente
        if "SIGAA" in driver.title:
            # Obtém o HTML da página
            html = driver.page_source

            # Salva o HTML em um arquivo
            with open('pagina.html', 'w', encoding='utf-8') as file:
                file.write(html)

            print("HTML baixado com sucesso.")
        else:
            print("Falha ao carregar a página.")
    finally:
        # Fecha o navegador
        driver.quit()

# Exemplo de uso
download_html('https://sigaa.unb.br/sigaa/public')
