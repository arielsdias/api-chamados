def calcular_prioridade(prioridade: str) -> int:
    prazos = {
        "alta": 4,
        "media": 24,
        "baixa": 72,
    }

    return prazos[prioridade]