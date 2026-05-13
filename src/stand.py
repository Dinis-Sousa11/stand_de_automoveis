from datetime import datetime
from utils import gerar_id
import json
import os

FICHEIRO_JSON="stands.json"


stands = {
    "S001": {"id": "S001", "nome": "Stand JDM Lisboa", "morada": "Rua do Motor, 1, Lisboa", "telefone": "210000001", "email": "lisboa@standjdm.pt", "nif": "500000001", "lista_ids_fornecedores": ["F001", "F002"], "data_registo": "2020-01-01 00:00:00"},
    "S002": {"id": "S002", "nome": "Stand JDM Porto", "morada": "Av. da Boavista, 200, Porto", "telefone": "220000002", "email": "porto@standjdm.pt", "nif": "500000002", "lista_ids_fornecedores": ["F002", "F003"], "data_registo": "2021-03-15 00:00:00"},
    "S003": {"id": "S003", "nome": "Stand JDM Faro", "morada": "Rua do Algarve, 5, Faro", "telefone": "289000003", "email": "faro@standjdm.pt", "nif": "500000003", "lista_ids_fornecedores": ["F001"], "data_registo": "2022-06-10 00:00:00"},
}

def _carregar_stands():
    if os.path.exists(FICHEIRO_JSON):
        with open(FICHEIRO_JSON, "r", encoding="utf-8") as f:
            return json.load(stands)
    return {}

def _guardar_stands():
    with open(FICHEIRO_JSON, "w", encoding="utf-8") as f:
        json.dump(stands, f, ensure_ascii=False, indent=2)

def criar_stand(nome, morada, telefone, email, nif):
    sid = gerar_id("stand")
    stands[sid] = {
        "id": sid,
        "nome": nome,
        "morada": morada,
        "telefone": telefone,
        "email": email,
        "nif": nif,
        "lista_ids_fornecedores": [],
        "data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return 201, stands[sid]

def listar_stands():
    if not stands:
        return 404, "Sem stands registados"
    return 200, stands

def obter_stand(sid):
    s = stands.get(sid)
    if not s:
        return 404, "Stand não encontrado"
    return 200, s

def atualizar_stand(sid, nome=None, morada=None, telefone=None,
                    email=None, lista_ids_fornecedores=None):
    s = stands.get(sid)
    if not s:
        return 404, "Stand não encontrado"
    if nome:                   s["nome"] = nome
    if morada:                 s["morada"] = morada
    if telefone:               s["telefone"] = telefone
    if email:                  s["email"] = email
    if lista_ids_fornecedores: s["lista_ids_fornecedores"] = lista_ids_fornecedores  # ✅ novo
    return 200, s

def remover_stand(sid):
    if sid not in stands:
        return 404, "Stand não encontrado"
    del stands[sid]
    return 200, sid
