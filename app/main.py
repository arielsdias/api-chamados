from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    Response,
    status as http_status,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from app.auth import criar_token, usuarios, validar_token


app = FastAPI(
    title="API de Gestão de Chamados Técnicos",
    description="API para registro e acompanhamento de chamados.",
    version="1.0.0",
)


@app.middleware("http")
async def registrar_requisicao(request: Request, call_next):
    print(
        f"Recebendo: {request.method} {request.url.path}"
    )

    response = await call_next(request)

    print(
        f"Respondendo: {response.status_code}"
    )

    return response


# -----------------------------
# MODELOS DE ENTRADA
# -----------------------------

class LoginEntrada(BaseModel):
    username: str


class ChamadoEntrada(BaseModel):
    titulo: str = Field(min_length=5, max_length=100)
    descricao: str
    prioridade: str = "baixa"


# -----------------------------
# DADOS EM MEMÓRIA
# -----------------------------

chamados = []
proximo_id = 1


# -----------------------------
# SEGURANÇA
# -----------------------------

security = HTTPBearer()


def obter_usuario_autenticado(
    credenciais: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        payload = validar_token(
            credenciais.credentials
        )

        return payload

    except ValueError as erro:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail=str(erro),
        )


# -----------------------------
# ROTAS BÁSICAS
# -----------------------------

@app.get("/")
def inicio():
    return {
        "mensagem": "API de Chamados funcionando!",
        "projeto": "Gestão de Chamados Técnicos",
    }


@app.get("/status")
def status():
    return {
        "status": "API está funcionando corretamente com sucesso"
    }


@app.get("/diagnostico")
def diagnostico():
    return {
        "status": "online",
        "diagnostico": "executado com sucesso",
    }


# -----------------------------
# PRAZO E RESUMO
# -----------------------------

def calcular_prazo(prioridade: str) -> int:
    prazos = {
        "alta": 4,
        "media": 24,
        "média": 24,
        "baixa": 72,
    }

    # prioridade = prioridade.strip().lower()

    if prioridade not in prazos:
        raise ValueError(
            f"Prioridade inválida: {prioridade}"
        )

    return prazos[prioridade]


def formatar_chamado(
    titulo: str,
    prioridade: str,
) -> str:
    return (
        f"[{prioridade.strip().upper()}] "
        f"{titulo.strip()}"
    )


@app.get("/resumo")
def resumo(
    titulo: str,
    prioridade: str,
):
    return {
        "titulo": titulo,
        "prioridade": prioridade,
        "resumo": formatar_chamado(
            titulo,
            prioridade,
        ),
    }


@app.get("/prazo/{prioridade}")
def consultar_prazo(prioridade: str):
    try:
        prazo = calcular_prazo(prioridade)

        return {
            "prioridade": prioridade,
            "prazo_em_horas": prazo,
        }

    except ValueError as erro:
        return {
            "erro": str(erro)
        }


# -----------------------------
# CRUD DE CHAMADOS
# -----------------------------

def buscar_chamado(id: int):
    for chamado in chamados:
        if chamado["id"] == id:
            return chamado

    raise HTTPException(
        status_code=http_status.HTTP_404_NOT_FOUND,
        detail="Chamado não encontrado",
    )


@app.post(
    "/chamados",
    status_code=http_status.HTTP_201_CREATED,
)
def criar_chamado(chamado: ChamadoEntrada):
    global proximo_id

    novo_chamado = {
        "id": proximo_id,
        **chamado.model_dump(),
    }

    chamados.append(novo_chamado)

    proximo_id += 1

    return novo_chamado


@app.get("/chamados")
def listar_chamados():
    return chamados


@app.get(
    "/chamados/{id}",
    summary="Buscar chamado por ID",
    description=(
        "Retorna os dados do chamado "
        "correspondente ao ID informado."
    ),
    tags=["Chamados"],
)
def obter_chamado(id: int):
    return buscar_chamado(id)


@app.put("/chamados/{id}")
def atualizar_chamado(
    id: int,
    dados: ChamadoEntrada,
):
    chamado = buscar_chamado(id)

    chamado.update(
        dados.model_dump()
    )

    return chamado


@app.delete(
    "/chamados/{id}",
    status_code=http_status.HTTP_204_NO_CONTENT,
)
def excluir_chamado(id: int):
    chamado = buscar_chamado(id)

    chamados.remove(chamado)

    return Response(
        status_code=http_status.HTTP_204_NO_CONTENT
    )


# -----------------------------
# LOGIN SIMPLIFICADO
# -----------------------------

@app.post("/login")
def login(dados: LoginEntrada):
    usuario = usuarios.get(
        dados.username
    )

    if not usuario:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inválido",
        )

    token = criar_token(
        usuario["username"],
        usuario["perfil"],
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "perfil": usuario["perfil"],
    }


# -----------------------------
# ROTAS PÚBLICA E PROTEGIDA
# -----------------------------

@app.get("/publico")
def publico():
    return {
        "mensagem": (
            "Esta rota é pública "
            "e não requer autenticação."
        )
    }


@app.get("/protegido")
def protegido(
    usuario: dict = Depends(
        obter_usuario_autenticado
    ),
):
    return {
        "mensagem": (
            f"Olá, {usuario['sub']}! "
            "Você acessou uma rota protegida."
        ),
        "perfil": usuario["perfil"],
    }