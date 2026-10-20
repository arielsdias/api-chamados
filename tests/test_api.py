from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_criar_chamado():
    resposta = client.post(
        "/chamados",
        json={
            "titulo": "Computador sem acesso",
            "descricao": "O computador não consegue acessar a rede.",
            "prioridade": "alta",
        },
    )

    assert resposta.status_code == 201

    chamado = resposta.json()
    assert chamado["titulo"] == "Computador sem acesso"
    assert chamado["descricao"] == "O computador não consegue acessar a rede."
    assert chamado["prioridade"] == "alta"
    assert "id" in chamado


def test_criar_chamado_com_titulo_invalido():
    resposta = client.post(
        "/chamados",
        json={
            "titulo": "PC",
            "descricao": "O computador não consegue acessar a rede.",
            "prioridade": "alta",
        },
    )

    assert resposta.status_code == 422