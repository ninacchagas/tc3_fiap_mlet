import streamlit as st
import pandas as pd
import numpy as np
import pyodbc
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
import io

st.title("📅 Previsão de Preços de Combustíveis")
st.text("""
Lembre-se de que esta aplicação foi criada para fins meramente educativos, é um entregável do Tech Challenge 3 do curso de Machine Learning Engineering da FIAP.
        
Esta aplicação tem como objetivo mostrar, de forma bem visual, as previsões dos valores dos combustíveis para a próxima semana.
""")

# Conexão com o banco e carregamento dos dados
server = 'beautyball\\SQLEXPRESS'
database = 'mlet-desafio'
conexao = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
)

conn = pyodbc.connect(conexao)

query = """
SELECT * FROM dbo.PRECOS_COMBUSTIVEL
"""

df_original = pd.read_sql(query, conn)

# Filtragem dos produtos que usou no treino
produtos_treinamento = [
    'ETANOL HIDRATADO',
    'GASOLINA ADITIVADA',
    'GASOLINA COMUM',
    'OLEO DIESEL'
]

df = df_original[df_original['PRODUTO'].isin(produtos_treinamento)].copy()

# Filtrando as colunas
colunas_df = ['DATA INICIAL', 'DATA FINAL', 'ESTADO', 'PRODUTO', 'PREÇO MÉDIO REVENDA']
df = df[colunas_df]

# Preprocessamento

# Label Encoding do ESTADO
le_estado = LabelEncoder()
df['COD_ESTADO'] = le_estado.fit_transform(df['ESTADO'])

# OneHotEncoding do PRODUTO
ohe_produto = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
produto_encoded = ohe_produto.fit_transform(df[['PRODUTO']])
df_produto_encoded = pd.DataFrame(produto_encoded, columns=ohe_produto.get_feature_names_out(['PRODUTO']))

df = pd.concat([df.reset_index(drop=True), df_produto_encoded], axis=1)

# Datas para datetime
df['DATA INICIAL'] = pd.to_datetime(df['DATA INICIAL'])
df['DATA FINAL'] = pd.to_datetime(df['DATA FINAL'])

# Criar semana, mês e ano
df['SEMANA'] = df['DATA FINAL'].dt.isocalendar().week
df['MES'] = df['DATA FINAL'].dt.month
df['ANO'] = df['DATA FINAL'].dt.year

# Ordena para usar shift
df = df.sort_values(['ESTADO', 'PRODUTO', 'ANO', 'SEMANA']).reset_index(drop=True)

# Cria colunas preço semanas anteriores
for i in range(1, 8):
    df[f'PRECO_SEMANA_MENOS_{i}'] = df.groupby(['ESTADO', 'PRODUTO'])['PREÇO MÉDIO REVENDA'].shift(i)

# Qtde dias na semana
df['QTDE_DIAS_SEMANA'] = (df['DATA FINAL'] - df['DATA INICIAL']).dt.days

# Drop colunas originais que não vamos usar
df = df.drop(columns=['DATA INICIAL', 'DATA FINAL', 'ESTADO', 'PRODUTO'])

# Drop linhas com NA
df = df.dropna().reset_index(drop=True)

# Separar X e y
X = df.drop(columns=['PREÇO MÉDIO REVENDA'])
y = df['PREÇO MÉDIO REVENDA']

# Standard scaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Treinar modelo (ou carregar o seu modelo se já treinou fora)
modelo = XGBRegressor(objective='reg:squarederror', random_state=42)
modelo.fit(X_scaled, y)

st.success("Modelo treinado com sucesso!")

# Mostrar gráfico: valores reais vs previstos (usando dados do treino)
y_pred_train = modelo.predict(X_scaled)

plt.figure(figsize=(10,5))
plt.plot(y.values, label='Valor Real', alpha=0.7)
plt.plot(y_pred_train, label='Valor Previsto', alpha=0.7)
plt.title('Valores Reais x Valores Previsto no Treino')
plt.xlabel('Amostras')
plt.ylabel('Preço Médio Revenda')
plt.legend()
st.pyplot(plt)

st.text("""
Gráfico mostrando a comparação entre os valores reais e os valores previstos, afim de demonstrar a eficácia do modelo.
""")

# Preparar dado da última semana para previsão da próxima semana

df_last = df_original[df_original['PRODUTO'].isin(produtos_treinamento)].copy()
df_last['DATA FINAL'] = pd.to_datetime(df_last['DATA FINAL'])

ultimo_registro = df_last.sort_values(['ESTADO', 'PRODUTO', 'DATA FINAL']).groupby(['ESTADO', 'PRODUTO']).tail(1).reset_index(drop=True)

ultimo_registro['SEMANA'] = ultimo_registro['DATA FINAL'].dt.isocalendar().week
ultimo_registro['MES'] = ultimo_registro['DATA FINAL'].dt.month
ultimo_registro['ANO'] = ultimo_registro['DATA FINAL'].dt.year

ultimo_registro['QTDE_DIAS_SEMANA'] = (pd.to_datetime(ultimo_registro['DATA FINAL']) - pd.to_datetime(ultimo_registro['DATA INICIAL'])).dt.days

ultimo_registro['COD_ESTADO'] = le_estado.transform(ultimo_registro['ESTADO'])

produto_ohe_array = ohe_produto.transform(ultimo_registro[['PRODUTO']])
df_produto_ohe = pd.DataFrame(produto_ohe_array, columns=ohe_produto.get_feature_names_out(['PRODUTO']))

ultimo_registro = pd.concat([ultimo_registro.reset_index(drop=True), df_produto_ohe], axis=1)

for i in range(1, 8):
    ultimo_registro[f'PRECO_SEMANA_MENOS_{i}'] = ultimo_registro['PREÇO MÉDIO REVENDA']

colunas_necessarias = X.columns.to_list()
df_previsao = ultimo_registro[colunas_necessarias]

X_pred_scaled = scaler.transform(df_previsao)

y_pred = modelo.predict(X_pred_scaled)

df_result = pd.DataFrame({
    'ESTADO': ultimo_registro['ESTADO'],
    'PRODUTO': ultimo_registro['PRODUTO'],
    'PREÇO ÚLTIMA SEMANA': ultimo_registro['PREÇO MÉDIO REVENDA'],
    'PREVISÃO PRÓXIMA SEMANA': y_pred
})

st.subheader("Previsão de preços para a próxima semana")
st.dataframe(df_result.style.format({
    'PREÇO ÚLTIMA SEMANA': '{:.4f}',
    'PREVISÃO PRÓXIMA SEMANA': '{:.4f}'
}))

# Botão para download CSV
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data = convert_df_to_csv(df_result)

st.download_button(
    label="Baixar tabela como CSV",
    data=csv_data,
    file_name='previsao_precos_combustiveis.csv',
    mime='text/csv',
)

