import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def baixar_arquivos():
    url_pagina = "https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/levantamento-de-precos-de-combustiveis-ultimas-semanas-pesquisadas"
    base_url = "https://www.gov.br"
    html = requests.get(url_pagina).text
    soup = BeautifulSoup(html, "html.parser")

    links_xlsx = []

    for link in soup.find_all("a", href=True):
        href = link['href']
        if ".xlsx" in href and '2025' in href and 'resumo_semanal' in href:
            links_xlsx.append(urljoin(base_url, href))

    print(f"{len(links_xlsx)} arquivos encontrados.")

    folder = os.path.join("stored-data", "raw_data_excel")
    os.makedirs(folder, exist_ok=True)

    for i, l in enumerate(links_xlsx):
        print('Baixando:', l)
        response = requests.get(l)
        file_path = os.path.join(folder, f"dados_semanais_{i}.xlsx")
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Arquivo salvo: {file_path}")