from datetime import datetime
from utils import gerar_id
import logging
log = logging.getLogger(__name__)
import json
import os

FICHEIRO_JSON = "fornecedores.json"
fornecedores = {}

def _carregar_fornecedores():
    global fornecedores
    if os.path.exists(FICHEIRO_JSON):
        with open(FICHEIRO_JSON, "r", encoding="utf-8") as f:
            fornecedores = json.load(f)
        log.debug(f"Fornecedores carregados do ficheiro ({len(fornecedores)} registos)")
    else:
        fornecedores = {}
        log.debug("Ficheiro fornecedores.json não existe, a usar dicionário vazio")
    return fornecedores

def _guardar_fornecedores():
    with open(FICHEIRO_JSON, "w", encoding="utf-8") as f:
        json.dump(fornecedores, f, ensure_ascii=False, indent=2)
    log.debug(f"Fornecedores guardados no ficheiro ({len(fornecedores)} registos)")


def criar_fornecedor(nome, contacto, pais, email, tipo, morada, avaliacao):
    log.info(f"Tentativa de criação de fornecedor: nome={nome}, país={pais}, tipo={tipo}")
    _carregar_fornecedores()
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
    log.info(f"Fornecedor criado com sucesso: {nome} ({pais}) | ID: {fid}")
    return 201, fornecedores[fid]

def listar_fornecedores():
    log.debug("A listar fornecedores")
    _carregar_fornecedores()
    if not fornecedores:
        log.info("Listagem de fornecedores: sem fornecedores registados")
        return 404, "Sem fornecedores registados"
    log.info(f"Fornecedores listados: {len(fornecedores)} registo(s)")
    return 200, fornecedores

def obter_fornecedor(fid):
    log.debug(f"A obter fornecedor com ID: {fid}")
    _carregar_fornecedores()
    f = fornecedores.get(fid)
    if not f:
        log.warning(f"Fornecedor não encontrado: {fid}")
        return 404, "Fornecedor não encontrado"
    log.debug(f"Fornecedor encontrado: {f['nome']} ({fid})")
    return 200, f

def atualizar_fornecedor(fid, nome=None, contacto=None, avaliacao=None, morada=None, nova_matricula=None):
    log.info(f"Tentativa de atualização do fornecedor: {fid}")
    _carregar_fornecedores()
    f = fornecedores.get(fid)
    if not f:
        log.warning(f"Atualização falhada — fornecedor não encontrado: {fid}")
        return 404, "Fornecedor não encontrado"
    if nome:           f["nome"] = nome
    if contacto:       f["contacto"] = contacto
    if avaliacao:      f["avaliacao"] = int(avaliacao)
    if morada:         f["morada"] = morada
    if nova_matricula:
        f["ids_carros"].append(nova_matricula)
        log.info(f"Matrícula '{nova_matricula}' adicionada ao fornecedor '{fid}'")
    _guardar_fornecedores()
    log.info(f"Fornecedor {fid} atualizado com sucesso")
    return 200, f

def remover_fornecedor(fid):
    log.info(f"Tentativa de remoção do fornecedor: {fid}")
    _carregar_fornecedores()
    if fid not in fornecedores:
        log.warning(f"Remoção falhada — fornecedor não encontrado: {fid}")
        return 404, "Fornecedor não encontrado"
    nome = fornecedores[fid]["nome"]
    del fornecedores[fid]
    _guardar_fornecedores()
    log.info(f"Fornecedor removido com sucesso: {nome} ({fid})")
    return 200, fid