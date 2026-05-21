from datetime import datetime
from utils import gerar_id, validar_data
from utils import log
import json
import os

FICHEIRO_JSON = "clientes.json"
clientes = {}

def _carregar_clientes():
    global clientes
    if os.path.exists(FICHEIRO_JSON):
        with open(FICHEIRO_JSON, "r", encoding="utf-8") as f:
            clientes = json.load(f)
        log.debug(f"Clientes carregados do ficheiro ({len(clientes)} registos)")
    else:
        clientes = {}
        log.debug("Ficheiro clientes.json não existe, a usar dicionário vazio")
    return clientes

def _guardar_clientes():
    with open(FICHEIRO_JSON, "w", encoding="utf-8") as f:
        json.dump(clientes, f, ensure_ascii=False, indent=2)
    log.debug(f"Clientes guardados no ficheiro ({len(clientes)} registos)")


def criar_cliente(nome, data_nascimento, telefone, email, preferencias, tipo_compra):
    log.info(f"Tentativa de criação de cliente: nome={nome}, email={email}, tipo={tipo_compra}")
    _carregar_clientes()
    if not validar_data(data_nascimento):
        log.warning(f"Data de nascimento inválida fornecida: '{data_nascimento}' para cliente '{nome}'")
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
    log.info(f"Cliente criado com sucesso: {nome} | ID: {cid}")
    return 201, clientes[cid]

def listar_clientes():
    log.debug("A listar clientes")
    _carregar_clientes()
    if not clientes:
        log.info("Listagem de clientes: sem clientes registados")
        return 404, "Sem clientes registados"
    log.info(f"Clientes listados: {len(clientes)} registo(s)")
    return 200, clientes

def obter_cliente(cid):
    log.debug(f"A obter cliente com ID: {cid}")
    _carregar_clientes()
    u = clientes.get(cid.upper())
    if not u:
        log.warning(f"Cliente não encontrado: {cid}")
        return 404, "Cliente não encontrado"
    log.debug(f"Cliente encontrado: {u['nome']} ({cid})")
    return 200, u

def atualizar_cliente(cid, nome=None, telefone=None, email=None, preferencias=None, tipo_compra=None):
    log.info(f"Tentativa de atualização do cliente: {cid}")
    _carregar_clientes()
    u = clientes.get(cid)
    if not u:
        log.warning(f"Atualização falhada — cliente não encontrado: {cid}")
        return 404, "Cliente não encontrado"
    if nome:         u["nome"] = nome
    if telefone:     u["telefone"] = telefone
    if email:        u["email"] = email
    if preferencias: u["preferencias"] = preferencias
    if tipo_compra:  u["tipo_compra"] = tipo_compra
    _guardar_clientes()
    log.info(f"Cliente {cid} atualizado com sucesso")
    return 200, cid

def remover_cliente(cid):
    log.info(f"Tentativa de remoção do cliente: {cid}")
    _carregar_clientes()
    if cid not in clientes:
        log.warning(f"Remoção falhada — cliente não encontrado: {cid}")
        return 404, "Cliente não encontrado"
    nome = clientes[cid]["nome"]
    del clientes[cid]
    _guardar_clientes()
    log.info(f"Cliente removido com sucesso: {nome} ({cid})")
    return 200, cid