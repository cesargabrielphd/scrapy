import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Configurar o driver do navegador (neste exemplo, ChromeDriver)
driver_path = "chrome/chrome.exe"  # Certifique-se de que este é o caminho correto para o novo ChromeDriver
service = Service(driver_path)
options = Options()
options.add_argument("--headless")  # Executa o Chrome em modo headless (sem interface gráfica)
driver = webdriver.Chrome(service=service, options=options)

# Abrir a página inicial
url = "https://sigaa.unb.br/sigaa/public/home.jsf"
driver.get(url)

# Esperar pelo carregamento completo da página inicial
input("Navegue até a página desejada e pressione Enter para iniciar a raspagem...")

# Obter o HTML da página carregada
html_content = driver.page_source

# Fechar o navegador
driver.quit()

# Analisar o HTML
soup = BeautifulSoup(html_content, "html.parser")

# Criar uma pasta para salvar os PDFs
os.makedirs("ementas", exist_ok=True)

# Iterar sobre as linhas da tabela e extrair as informações
for row in soup.select("tbody tr"):
    codigo = row.select_one("td:nth-child(1)").text
    nome = row.select_one("td:nth-child(2)").text
    tipo = row.select_one("td:nth-child(3)").text
    ch_total = row.select_one("td:nth-child(4)").text
    ementa_link = row.select_one("td:nth-child(5) a")["href"]

    # Verificar se a URL é válida
    if ementa_link == "#":
        print(f"Ignorando link inválido para {nome}")
        continue

    if not ementa_link.startswith("http"):
        ementa_link = "https://sigaa.unb.br/sigaa/public/" + ementa_link.lstrip(
            "/"
        )  # Adiciona o domínio base

    # Fazer o download do PDF da ementa
    pdf_response = requests.get(ementa_link)
    pdf_response.raise_for_status()

    # Salvar o PDF na pasta 'ementas'
    pdf_path = os.path.join("ementas", f"{codigo}_{nome}.pdf")
    with open(pdf_path, "wb") as pdf_file:
        pdf_file.write(pdf_response.content)

    print(
        f"Código: {codigo}, Nome: {nome}, Tipo: {tipo}, CH Total: {ch_total} - Ementa baixada: {pdf_path}"
    )

print("Download das ementas concluído.")
