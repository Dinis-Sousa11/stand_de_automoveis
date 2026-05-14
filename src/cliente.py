from datetime import datetime
from utils import gerar_id, validar_data
import json
import os

FICHEIRO_JSON = "clientes.json"

clientes = {}

def _carregar_clientes():
    if os.path.exists(FICHEIRO_JSON):
        with open(FICHEIRO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def _guardar_clientes():
    with open(FICHEIRO_JSON, "w", encoding="utf-8") as f:
        json.dump(clientes, f, ensure_ascii=False, indent=2)

clientes = _carregar_clientes()


def criar_cliente(nome, data_nascimento, telefone, email, preferencias, tipo_compra):
    if not validar_data(data_nascimento):
        return 400, "Data inválida. Use formato YYYY-MM-DD"
    cid = gerar_id("cliente")
    clientes[cid] = {
        "id": cid,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "telefone": telefone,
        "email": email,
        "preferencias": preferencias,
        "tipo_compra": tipo_compra,
        "saldo": 0.0,
        "carros": [],
        "data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    _guardar_clientes()
    return 201, clientes[cid]

def listar_clientes():
    if not clientes:
        return 404, "Sem clientes registados"
    return 200, clientes

def obter_cliente(cid):
    u = clientes.get(cid.upper())
    if not u:
        return 404, "Cliente não encontrado"
    return 200, u

def atualizar_cliente(cid, nome=None, telefone=None, email=None, preferencias=None, tipo_compra=None):
    u = clientes.get(cid)
    if not u:
        return 404, "Cliente não encontrado"
    if nome:         u["nome"] = nome
    if telefone:     u["telefone"] = telefone
    if email:        u["email"] = email
    if preferencias: u["preferencias"] = preferencias
    if tipo_compra:  u["tipo_compra"] = tipo_compra
    _guardar_clientes()
    return 200, cid

def remover_cliente(cid):
    if cid not in clientes:
        return 404, "Cliente não encontrado"
    del clientes[cid]
    _guardar_clientes()
    return 200, cid