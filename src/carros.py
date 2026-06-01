from datetime import datetime
from utils import gerar_id
from utils import log
import json
import os

FICHEIRO_JSON = "carros.json"
carros = {}

def _carregar_carros():
    global carros
    if os.path.exists(FICHEIRO_JSON):
        with open(FICHEIRO_JSON, "r", encoding="utf-8") as f:
            carros = json.load(f)
        log.debug(f"Carros carregados do ficheiro ({len(carros)} registos)")
    else:
        carros = {}
        log.debug("Ficheiro carros.json não existe, a usar dicionário vazio")

def _guardar_carros():
    with open(FICHEIRO_JSON, "w", encoding="utf-8") as f:
        json.dump(carros, f, ensure_ascii=False, indent=2)
    log.debug(f"Carros guardados no ficheiro ({len(carros)} registos)")


def criar_carro(matricula, marca, modelo, ano, preco, kms, cor,
                tracao, num_portas, cilindrada, potencia, lotacao, id_stand, id_fornecedor):
    log.info(f"Tentativa de criação de carro: matrícula={matricula}, marca={marca}, modelo={modelo}, stand={id_stand}, fornecedor={id_fornecedor}")
    _carregar_carros()
    if matricula in carros:
        log.error(f"Carro com matrícula '{matricula}' já existe no sistema")
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
    log.info(f"Carro criado com sucesso: {marca} {modelo} ({matricula}) | Preço: {preco}€ | Stand: {id_stand}")
    return 201, carro

def listar_stock():
    log.debug("A listar stock disponível")
    _carregar_carros()
    disponiveis = {m: c for m, c in carros.items() if not c["id_cliente"]}
    if not disponiveis:
        log.error("Listagem de stock: sem carros disponíveis")
        return 404, {}
    log.info(f"Stock listado: {len(disponiveis)} carro(s) disponível(is)")
    return 200, disponiveis

def obter_carro(matricula):
    log.debug(f"A obter carro com matrícula: {matricula}")
    _carregar_carros()
    carro = carros.get(matricula.upper())
    if not carro:
        log.error(f"Carro não encontrado: {matricula}")
        return 404, "Não encontrado"
    log.debug(f"Carro encontrado: {carro['marca']} {carro['modelo']} ({matricula})")
    return 200, carro

def atualizar_carro(matricula, marca=None, modelo=None, ano=None,
                    preco=None, kms=None, cor=None, id_cliente=None):
    log.info(f"Tentativa de atualização do carro: {matricula}")
    _carregar_carros()
    carro = carros.get(matricula.upper())
    if not carro:
        log.error(f"Atualização falhada — carro não encontrado: {matricula}")
        return 404, "Carro não encontrado"
    if marca:      carro["marca"] = marca
    if modelo:     carro["modelo"] = modelo
    if ano:        carro["ano"] = ano
    if preco:      carro["preco"] = preco
    if kms:        carro["kms"] = kms
    if cor:        carro["cor"] = cor
    if id_cliente:
        carro["id_cliente"] = id_cliente
        log.info(f"Carro {matricula} associado ao cliente {id_cliente}")
    _guardar_carros()
    log.info(f"Carro {matricula} atualizado com sucesso")
    return 200, carro

def remover_carro(matricula):
    log.info(f"Tentativa de remoção do carro: {matricula}")
    _carregar_carros()
    carro = carros.get(matricula.upper())
    if not carro:
        log.error(f"Remoção falhada — carro não encontrado: {matricula}")
        return 404, "Carro não encontrado"
    if carro["id_cliente"]:
        log.error(f"Remoção falhada — carro {matricula} já tem dono (cliente: {carro['id_cliente']})")
        return 400, "Carro já tem dono"
    del carros[matricula.upper()]
    _guardar_carros()
    log.info(f"Carro removido com sucesso: {matricula}")
    return 200, matricula