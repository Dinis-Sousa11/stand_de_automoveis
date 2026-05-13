from datetime import datetime
from utils import gerar_id
import json
import os

FICHEIRO_JSON = "fornecedores.json"


def _carregar_fornecedores():
    if os.path.exists(FICHEIRO_JSON):
        with open(FICHEIRO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return 200

def _guardar_fornecedores():
    with open(FICHEIRO_JSON, "w", encoding="utf-8") as f:
        json.dump(fornecedores, f, ensure_ascii=False, indent=2)

fornecedores = _carregar_fornecedores()


def criar_fornecedor(nome, contacto, pais, email, tipo, morada, avaliacao):
    fid = gerar_id("fornecedor")
    fornecedores[fid] = {
        "id": fid,
        "nome": nome,
        "contacto": contacto,
        "pais": pais,
        "email": email,
        "tipo": tipo,
        "morada": morada,
        "avaliacao": int(avaliacao),
        "ids_carros": [],
        "data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    _guardar_fornecedores()
    return 201, fornecedores[fid]

def listar_fornecedores():
    if not fornecedores:
        return 404, "Sem fornecedores registados"
    return 200, fornecedores

def obter_fornecedor(fid):
    f = fornecedores.get(fid)
    if not f:
        return 404, "Fornecedor não encontrado"
    return 200, f

def atualizar_fornecedor(fid, nome=None, contacto=None, avaliacao=None,
                          morada=None, nova_matricula=None):
    f = fornecedores.get(fid)
    if not f:
        return 404, "Fornecedor não encontrado"
    if nome:           f["nome"] = nome
    if contacto:       f["contacto"] = contacto
    if avaliacao:      f["avaliacao"] = int(avaliacao)
    if morada:         f["morada"] = morada
    if nova_matricula: f["ids_carros"].append(nova_matricula)
    _guardar_fornecedores()
    return 200, f

def remover_fornecedor(fid):
    if fid not in fornecedores:
        return 404, "Fornecedor não encontrado"
    del fornecedores[fid]
    _guardar_fornecedores()
    return 200, fid
