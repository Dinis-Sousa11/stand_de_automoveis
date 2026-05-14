from datetime import datetime
from utils import gerar_id
import json
import os

FICHEIRO_JSON = "carros.json"
carros = {}

def _carregar_carros():
    global carros
    if os.path.exists(FICHEIRO_JSON):
        with open(FICHEIRO_JSON, "r", encoding="utf-8") as f:
            carros = json.load(f)
    else:
        carros = {}

def _guardar_carros():
    with open(FICHEIRO_JSON, "w", encoding="utf-8") as f:
        json.dump(carros, f, ensure_ascii=False, indent=2)




def criar_carro(matricula, marca, modelo, ano, preco, kms, cor,
                tracao, num_portas, cilindrada, potencia, lotacao, id_stand, id_fornecedor):
    _carregar_carros()
    if matricula in carros:
        return 400, "Já existe um carro com essa matrícula."
    carro = {
        "matricula": matricula,
        "marca": marca,
        "modelo": modelo,
        "ano": int(ano),
        "preco": float(preco),
        "kms": int(kms),
        "cor": cor,
        "tracao": tracao,
        "num_portas": int(num_portas),
        "cilindrada": float(cilindrada),
        "potencia": int(potencia),
        "lotacao": int(lotacao),
        "id_stand": id_stand,
        "id_fornecedor": id_fornecedor,
        "id_cliente": None,
        "data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    carros[matricula] = carro
    _guardar_carros()
    return 201, carro

def listar_stock():
    _carregar_carros()
    disponiveis = {m: c for m, c in carros.items() if not c["id_cliente"]}
    if not disponiveis:
        return 404, {}
    return 200, disponiveis

def obter_carro(matricula):
    _carregar_carros()
    carro = carros.get(matricula.upper())
    if not carro:
        return 404, "Não encontrado"
    return 200, carro

def atualizar_carro(matricula, marca=None, modelo=None, ano=None,
                    preco=None, kms=None, cor=None, id_cliente=None):
    _carregar_carros()
    carro = carros.get(matricula.upper())
    if not carro:
        return 404, "Carro não encontrado"
    if marca:      carro["marca"] = marca
    if modelo:     carro["modelo"] = modelo
    if ano:        carro["ano"] = ano
    if preco:      carro["preco"] = preco
    if kms:        carro["kms"] = kms
    if cor:        carro["cor"] = cor
    if id_cliente: carro["id_cliente"] = id_cliente
    _guardar_carros()
    return 200, carro

def remover_carro(matricula):
    _carregar_carros()
    carro = carros.get(matricula.upper())
    if not carro:
        return 404, "Carro não encontrado"
    if carro["id_cliente"]:
        return 400, "Carro já tem dono"
    del carros[matricula.upper()]
    _guardar_carros()
    return 200, matricula