import pytest 
from src import storage

def test_inicializacao_json(tmp_path):
    # TEste 1: Garante que iniciou zerado se o arquivo não existir
    arquivo_temp = tmp_path / "teste.json"
    dados = storage.load_data(arquivo_temp)
    assert dados["agua_ml"] == 0
    assert len(dados["medicamentos"]) == 0

def test_add_medicamento(tmp_path): 
    # Teste 2: Caminho para ser feliz
    arquivo_temp = tmp_path / "teste.json"
    storage.add_medicamento("Losartana", "08:00", arquivo_temp)
    dados = storage.load_data(arquivo_temp)
    assert len(dados["medicamentos"]) == 1
    assert dados["medicamentos"][0]["nome"] == "Losartana"

def test_add_agua_invalida(tmp_path):
    # Teste 3: Caso limite / Erro
    arquivo_temp = tmp_path / "teste.json"
    with pytest.raises(ValueError):
        storage.add_agua(0, arquivo_temp) #Feito para não aceitar 0ml