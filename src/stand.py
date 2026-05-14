from datetime import datetime
from utils import gerar_id
import json
import os

FICHEIRO_JSON = "stands.json"

stands = {}

def _carregar_stands():
    global stands
    if os.path.exists(FICHEIRO_JSON):
        with open(FICHEIRO_JSON, "r", encoding="utf-8") as f:
            stands = json.load(f)
    return stands

def _guardar_stands():
    with open(FICHEIRO_JSON, "w", encoding="utf-8") as f:
        json.dump(stands, f, ensure_ascii=False, indent=2)


def criar_stand(nome, morada, telefone, email, nif):
    _carregar_stands()
    sid = gerar_id("stand")
    stands[sid] = {
        "id": sid, "nome": nome, "morada": morada,
        "telefone": telefone, "email": email, "nif": nif,
        "lista_ids_fornecedores": [],
        "data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    _guardar_stands()
    return 201, stands[sid]

def listar_stands():
    _carregar_stands()
    if not stands:
        return 404, "Sem stands registados"
    return 200, stands

def obter_stand(sid):
    _carregar_stands()
    s = stands.get(sid)
    if not s:
        return 404, "Stand não encontrado"
    return 200, s

def atualizar_stand(sid, nome=None, morada=None, telefone=None,
                    email=None, lista_ids_fornecedores=None):
    _carregar_stands()
    s = stands.get(sid)
    if not s:
        return 404, "Stand não encontrado"
    if nome:                   s["nome"] = nome
    if morada:                 s["morada"] = morada
    if telefone:               s["telefone"] = telefone
    if email:                  s["email"] = email
    if lista_ids_fornecedores: s["lista_ids_fornecedores"] = lista_ids_fornecedores
    _guardar_stands()
    return 200, s

def remover_stand(sid):
    _carregar_stands()
    if sid not in stands:
        return 404, "Stand não encontrado"
    del stands[sid]
    _guardar_stands()
    return 200, sid