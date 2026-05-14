from datetime import datetime
import json
import os

FICHEIRO_JSON= "fornecimentos.json"

fornecimentos = {}
_contador = 1

def _carregar_fornecimentos():
    global fornecimentos
    if os.path.exists(FICHEIRO_JSON):
        with open(FICHEIRO_JSON, "r", encoding="utf-8") as f:
            fornecimentos = json.load(f)
    return fornecimentos

def _guardar_fornecimentos():
    with open(FICHEIRO_JSON, "w", encoding="utf-8") as f:
        json.dump(fornecimentos, f, ensure_ascii=False, indent=2)


def _gerar_id():
    global _contador
    fid = f"FO{_contador:03d}"
    _contador += 1
    return fid

# CREATE
def criar_fornecimento(id_stand, id_fornecedor):
    _carregar_fornecimentos()
    for fo in fornecimentos.values():
        if fo["id_stand"] == id_stand and fo["id_fornecedor"] == id_fornecedor:
            return 400, "Fornecimento já existe"
    foid = _gerar_id()
    fornecimentos[foid] = {
        "id": foid,
        "id_stand": id_stand,
        "id_fornecedor": id_fornecedor,
        "data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    _guardar_fornecimentos()
    return 201, fornecimentos[foid]

# READ
def listar_fornecimentos():
    _carregar_fornecimentos()
    if not fornecimentos:
        return 404, "Sem fornecimentos registados"
    return 200, fornecimentos

def obter_fornecimento(foid):
    _carregar_fornecimentos()
    fo = fornecimentos.get(foid)
    if not fo:
        return 404, "Fornecimento não encontrado"
    return 200, fo

# DELETE
def remover_fornecimento(foid):
    _carregar_fornecimentos()
    if foid not in fornecimentos:
        return 404, "Fornecimento não encontrado"
    del fornecimentos[foid]
    _guardar_fornecimentos()
    return 200, foid
