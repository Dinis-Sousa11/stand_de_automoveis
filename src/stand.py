from datetime import datetime
from utils import gerar_id
import logging
log = logging.getLogger(__name__)
import json
import os

FICHEIRO_JSON = "stands.json"
stands = {}

def _carregar_stands():
    global stands
    if os.path.exists(FICHEIRO_JSON):
        with open(FICHEIRO_JSON, "r", encoding="utf-8") as f:
            stands = json.load(f)
        log.debug(f"Stands carregados do ficheiro ({len(stands)} registos)")
    else:
        stands = {}
        log.debug("Ficheiro stands.json não existe, a usar dicionário vazio")
    return stands

def _guardar_stands():
    with open(FICHEIRO_JSON, "w", encoding="utf-8") as f:
        json.dump(stands, f, ensure_ascii=False, indent=2)
    log.debug(f"Stands guardados no ficheiro ({len(stands)} registos)")


def criar_stand(nome, morada, telefone, email, nif):
    log.info(f"Tentativa de criação de stand: nome={nome}, morada={morada}")
    _carregar_stands()
    sid = gerar_id("stand")
    stands[sid] = {
        "id": sid, "nome": nome, "morada": morada,
        "telefone": telefone, "email": email, "nif": nif,
        "lista_ids_fornecedores": [],
        "data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    _guardar_stands()
    log.info(f"Stand criado com sucesso: {nome} | ID: {sid} | Morada: {morada}")
    return 201, stands[sid]

def listar_stands():
    log.debug("A listar stands")
    _carregar_stands()
    if not stands:
        log.info("Listagem de stands: sem stands registados")
        return 404, "Sem stands registados"
    log.info(f"Stands listados: {len(stands)} registo(s)")
    return 200, stands

def obter_stand(sid):
    log.debug(f"A obter stand com ID: {sid}")
    _carregar_stands()
    s = stands.get(sid)
    if not s:
        log.warning(f"Stand não encontrado: {sid}")
        return 404, "Stand não encontrado"
    log.debug(f"Stand encontrado: {s['nome']} ({sid})")
    return 200, s

def atualizar_stand(sid, nome=None, morada=None, telefone=None,
                    email=None, lista_ids_fornecedores=None):
    log.info(f"Tentativa de atualização do stand: {sid}")
    _carregar_stands()
    s = stands.get(sid)
    if not s:
        log.warning(f"Atualização falhada — stand não encontrado: {sid}")
        return 404, "Stand não encontrado"
    if nome:                   s["nome"] = nome
    if morada:                 s["morada"] = morada
    if telefone:               s["telefone"] = telefone
    if email:                  s["email"] = email
    if lista_ids_fornecedores:
        s["lista_ids_fornecedores"] = lista_ids_fornecedores
        log.debug(f"Stand {sid}: lista de fornecedores atualizada → {lista_ids_fornecedores}")
    _guardar_stands()
    log.info(f"Stand {sid} atualizado com sucesso")
    return 200, s

def remover_stand(sid):
    log.info(f"Tentativa de remoção do stand: {sid}")
    _carregar_stands()
    if sid not in stands:
        log.warning(f"Remoção falhada — stand não encontrado: {sid}")
        return 404, "Stand não encontrado"
    nome = stands[sid]["nome"]
    del stands[sid]
    _guardar_stands()
    log.info(f"Stand removido com sucesso: {nome} ({sid})")
    return 200, sid