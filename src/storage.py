import json
import os

FILE_PATH = "data.json"

def load_data(file_path=FILE_PATH):
    if not os.path.exists(file_path):
     return {"medicamentos": [], "agua_ml": 0}

    with open(file_path, "r", encoding="utf-8" ) as f:
        return json.load(f)

def save_data(data, file_path=FILE_PATH):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_medicamento(nome, horario, file_path=FILE_PATH):
    data = load_data(file_path)
    data["medicamentos"].append({
        "nome": nome,
        "horario": horario,
        "concluido": False
    })
    save_data(data, file_path)

def add_agua(ml, file_path=FILE_PATH):
    if ml <= 0:
        raise ValueError("A quantidade de água deve ser maior que zero.")
    data = load_data(file_path)
    data["agua_ml"] += ml
    save_data(data, file_path)
