# Predição de preço de combustível por estado

> Projeto criado com fim educativo, apenas. Trata-se do projeto destinado ao terceiro Tech Challenge da Pós Graduação da FIAP, para o curso de Machine Learning Engineering.

### ❓ Sobre o projeto:

O projeto desenvolvido conta com a base de dados da ANP - Agência Nacional de Petróleo. Estes dados foram extraídos do link (https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/levantamento-de-precos-de-combustiveis-ultimas-semanas-pesquisadas), este que conta com o histórico semanal do valor dos combustíveis em cada estado brasileiro. 

## 🔧 Etapas do Projeto

1. 📥 **Coleta de dados**  
   - Foi criado o arquivo scraper.py, responsável por realizar o scraping dos dados diretamente da página da ANP. Esse script implementa um pipeline completo de ETL: os dados são extraídos da página oficial (scraper.py), transformados(transform.py) (visto que os arquivos vêm em formato Excel com uma estrutura padronizada), e então carregados em uma base de dados SQL Server (database.py).
   - A coleta foi configurada para extrair apenas os dados referentes ao ano de 2025.
   - Todo o processo de ETL foi encapsulado em uma API, que executa as etapas de forma automatizada (main.py).

2. 🧹 **Pré-processamento**  
   - Com os dados já disponíveis no SQL Server, iniciou-se a etapa de pré-processamento. Nela, foram feitas padronizações de colunas, tratamento de valores ausentes e conversões necessárias de tipo de dado. Essas transformações garantiram que os dados estivessem prontos para alimentar o modelo de machine learning.

3. 📊 **Análise exploratória (EDA)**  
   - A análise exploratória teve como objetivo entender a estrutura dos dados e selecionar as variáveis mais relevantes para o modelo. As principais colunas identificadas foram: estado, produto, valor médio, data inicial (semana de início) e data final (semana de término). Essa etapa foi fundamental para validar a qualidade e a consistência das informações.

4. 📈 **Treinamento do modelo**  
   - O modelo foi treinado utilizando o algoritmo XGBoost. Embora algoritmos como o Prophet sejam recomendados para séries temporais, optou-se pelo XGBoost devido à sua flexibilidade em lidar com múltiplas variáveis categóricas e temporais.
   - Essa abordagem permitiu utilizar não apenas o histórico de preços, mas também informações como estado e tipo de combustível, aumentando a capacidade preditiva do modelo para contextos específicos.

5. 🌐 **Construção do app em Streamlit**  
   - A etapa final foi a criação de um aplicativo interativo utilizando Streamlit.
   - O app apresenta, de forma visual e acessível, os resultados das previsões geradas pelo modelo. Ele exibe uma tabela com: nome do estado, semana analisada, tipo de combustível, valor atual e previsão da semana seguinte.
   - Os resultados podem ser exportados em .csv, e o app também demonstra a performance do modelo com métricas de avaliação.

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:

   - Você possui o Python 3.10+ instalado em sua máquina.

   - Você possui um ambiente virtual configurado (recomendado).

   - Você possui acesso a um banco de dados SQL Server com as permissões adequadas.

   - Você executou o comando abaixo para instalar todas as dependências necessárias do projeto:
   ```<pip install -r requirements.txt>```

## 🚀 Instalando o projeto

Clone o repositório e instale as dependências:

```git clone <URL-do-repositório>```
```cd <nome-do-diretório>```
```pip install -r requirements.txt```

   - Certifique-se de configurar corretamente as variáveis de ambiente, como string de conexão com o banco de dados.

## ☕ Usando o projeto
   - Executar a API (processo de ETL)

```uvicorn main:app --reload```

   - Acesse via navegador: http://127.0.0.1:8000/docs
   - Lá você verá a documentação interativa da API (via Swagger).


## 📊 Executar o app em Streamlit

```streamlit run app.py```

   - Esse comando irá abrir automaticamente o aplicativo no navegador, com visualizações e previsões de preço de combustível por estado.

