import pytest

from app.regras import calcular_prioridade


def test_calcular_prioridade_alta():
    assert calcular_prioridade("alta") == 4


def test_calcular_prioridade_media():
    assert calcular_prioridade("media") == 24


def test_calcular_prioridade_baixa():
    assert calcular_prioridade("baixa") == 72


def test_calcular_prioridade_urgente():
    with pytest.raises(KeyError):
        calcular_prioridade("urgente")


def test_calcular_prioridade_vazia():
    with pytest.raises(KeyError):
        calcular_prioridade("")


def test_calcular_prioridade_com_maiusculas():
    with pytest.raises(KeyError):
        calcular_prioridade("Alta")