from datetime import datetime
from utils import log
import json
import os

FICHEIRO_JSON = "fornecimentos.json"
fornecimentos = {}
_contador = 1

def _carregar_fornecimentos():
    global fornecimentos
    if os.path.exists(FICHEIRO_JSON):
        with open(FICHEIRO_JSON, "r", encoding="utf-8") as f:
            fornecimentos = json.load(f)
        log.debug(f"Fornecimentos carregados do ficheiro ({len(fornecimentos)} registos)")
    else:
        fornecimentos = {}
        log.debug("Ficheiro fornecimentos.json não existe, a usar dicionário vazio")
    return fornecimentos

def _guardar_fornecimentos():
    with open(FICHEIRO_JSON, "w", encoding="utf-8") as f:
        json.dump(fornecimentos, f, ensure_ascii=False, indent=2)
    log.debug(f"Fornecimentos guardados no ficheiro ({len(fornecimentos)} registos)")

def _gerar_id():
    global _contador
    fid = f"FO{_contador:03d}"
    _contador += 1
    log.debug(f"ID de fornecimento gerado: {fid}")
    return fid


def criar_fornecimento(id_stand, id_fornecedor):
    log.info(f"Tentativa de criação de fornecimento: stand={id_stand}, fornecedor={id_fornecedor}")
    _carregar_fornecimentos()
    for fo in fornecimentos.values():
        if fo["id_stand"] == id_stand and fo["id_fornecedor"] == id_fornecedor:
            log.error(f"Fornecimento duplicado: stand={id_stand} já tem fornecedor={id_fornecedor}")
            return 400, "Fornecimento já existe"
    foid = _gerar_id()
    fornecimentos[foid] = {
        "id": foid,
        "id_stand": id_stand,
        "id_fornecedor": id_fornecedor,
        "data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    _guardar_fornecimentos()
    log.info(f"Fornecimento criado com sucesso: {foid} | Stand: {id_stand} | Fornecedor: {id_fornecedor}")
    return 201, fornecimentos[foid]

def listar_fornecimentos():
    log.debug("A listar fornecimentos")
    _carregar_fornecimentos()
    if not fornecimentos:
        log.info("Listagem de fornecimentos: sem fornecimentos registados")
        return 404, "Sem fornecimentos registados"
    log.info(f"Fornecimentos listados: {len(fornecimentos)} registo(s)")
    return 200, fornecimentos

def obter_fornecimento(foid):
    log.debug(f"A obter fornecimento com ID: {foid}")
    _carregar_fornecimentos()
    fo = fornecimentos.get(foid)
    if not fo:
        log.error(f"Fornecimento não encontrado: {foid}")
        return 404, "Fornecimento não encontrado"
    log.debug(f"Fornecimento encontrado: {foid}")
    return 200, fo

def remover_fornecimento(foid):
    log.info(f"Tentativa de remoção do fornecimento: {foid}")
    _carregar_fornecimentos()
    if foid not in fornecimentos:
        log.error(f"Remoção falhada — fornecimento não encontrado: {foid}")
        return 404, "Fornecimento não encontrado"
    del fornecimentos[foid]
    _guardar_fornecimentos()
    log.info(f"Fornecimento removido com sucesso: {foid}")
    return 200, foid