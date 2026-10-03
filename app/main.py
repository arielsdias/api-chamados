from fastapi import FastAPI

app = FastAPI(
    title="API de Gestão de Chamados Técnicos",
    description="API para registro e acompanhamento de chamados.",
    version="1.0.0"
)

@app.get("/")
def inicio():
    return {
        "mensagem": "API de Chamados funcionando!",
        "projeto": "Gestão de Chamados Técnicos"
    }
