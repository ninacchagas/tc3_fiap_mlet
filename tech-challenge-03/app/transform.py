# Importando as bibliotecas 

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import date
import requests
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import openpyxl
import os

def transformar_dados():
    # Caminho para a pasta RAW e REFINED
    path_raw = 'stored-data\\raw_data_excel\\'
    path_refined = 'stored-data\\refined_data_excel\\'

    # Garante que a pasta de destino existe
    os.makedirs(path_refined, exist_ok=True)

    # Lista de arquivos no diretório RAW
    objetos_no_path = os.listdir(path_raw)

    for i, d in enumerate(objetos_no_path):
        input_path = os.path.join(path_raw, d)

        try:
            # Lê o Excel pulando as 9 primeiras linhas
            df = pd.read_excel(input_path, skiprows=9)

            # Caminho do arquivo de saída
            output_filename = f"dados_semanais_refined_{i}.xlsx"
            output_path = os.path.join(path_refined, output_filename)

            # Salva o DataFrame como .xlsx
            df.to_excel(output_path, index=False)

            print(f"Arquivo salvo como {output_path}")
        except Exception as e:
            print(f"Erro ao processar {input_path}: {e}")
