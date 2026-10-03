
# API de Gestão de Chamados Técnicos

API backend para registro e acompanhamento de
chamados de suporte técnico.

## Tecnologias

- Python
- FastAPI
- Uvicorn
- Git e GitHub

## Configuração do ambiente

Criar o ambiente virtual:

    python -m venv .venv

Ativar no PowerShell:

    .\.venv\Scripts\Activate.ps1

Instalar as dependências:

    python -m pip install -r requirements.txt

## Executar a aplicação

    python -m uvicorn app.main:app --reload

## Endereços

API: http://127.0.0.1:8000

Documentação: http://127.0.0.1:8000/docs
