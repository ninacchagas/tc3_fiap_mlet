from fastapi import FastAPI
from scraper import baixar_arquivos      
from transform import transformar_dados
from database import inserir_dados_sql

app = FastAPI()

@app.post("/atualizar-dados")
def atualizar_dados():
    try:
        baixar_arquivos()   
        transformar_dados()    
        inserir_dados_sql()   

        return {"status": "sucesso", "mensagem": "Dados atualizados com sucesso"}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

if __name__ == "__main__":
    app.run(debug=True)