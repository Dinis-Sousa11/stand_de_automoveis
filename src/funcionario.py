from datetime import datetime
from utils import gerar_id
from utils import log
import json
import os

FICHEIRO_JSON = "funcionarios.json"
funcionarios = {}

def _carregar_funcionarios():
    global funcionarios
    if os.path.exists(FICHEIRO_JSON):
        with open(FICHEIRO_JSON, "r", encoding="utf-8") as f:
            funcionarios = json.load(f)
        log.debug(f"Funcionários carregados do ficheiro ({len(funcionarios)} registos)")
    else:
        funcionarios = {}
        log.debug("Ficheiro funcionarios.json não existe, a usar dicionário vazio")
    return funcionarios

def _guardar_funcionarios():
    with open(FICHEIRO_JSON, "w", encoding="utf-8") as f:
        json.dump(funcionarios, f, ensure_ascii=False, indent=2)
    log.debug(f"Funcionários guardados no ficheiro ({len(funcionarios)} registos)")


def criar_funcionario(nome, cargo, salario, telefone, turno, nif, iban, id_stand):
    log.info(f"Tentativa de criação de funcionário: nome={nome}, cargo={cargo}, stand={id_stand}")
    _carregar_funcionarios()
    fid = gerar_id("funcionario")
    funcionarios[fid] = {
        "id": fid,
        "nome": nome,
        "cargo": cargo,
        "salario": float(salario),
        "telefone": telefone,
        "turno": turno,
        "nif": nif,
        "iban": iban,
        "id_stand": id_stand,
        "avaliacao": 0,
        "vendas_realizadas": [],
        "data_entrada": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    _guardar_funcionarios()
    log.info(f"Funcionário criado com sucesso: {nome} | Cargo: {cargo} | ID: {fid} | Stand: {id_stand}")
    return 201, funcionarios[fid]

def listar_funcionarios():
    log.debug("A listar funcionários")
    _carregar_funcionarios()
    if not funcionarios:
        log.info("Listagem de funcionários: sem funcionários registados")
        return 404, "Sem funcionários registados"
    log.info(f"Funcionários listados: {len(funcionarios)} registo(s)")
    return 200, funcionarios

def obter_funcionario(fid):
    log.debug(f"A obter funcionário com ID: {fid}")
    _carregar_funcionarios()
    f = funcionarios.get(fid)
    if not f:
        log.error(f"Funcionário não encontrado: {fid}")
        return 404, "Funcionário não encontrado"
    log.debug(f"Funcionário encontrado: {f['nome']} ({fid})")
    return 200, f

def atualizar_funcionario(fid, nome=None, cargo=None, salario=None, turno=None, avaliacao=None):
    log.info(f"Tentativa de atualização do funcionário: {fid}")
    _carregar_funcionarios()
    f = funcionarios.get(fid)
    if not f:
        log.error(f"Atualização falhada — funcionário não encontrado: {fid}")
        return 404, "Funcionário não encontrado"
    if nome:      f["nome"] = nome
    if cargo:     f["cargo"] = cargo
    if salario:   f["salario"] = float(salario)
    if turno:     f["turno"] = turno
    if avaliacao: f["avaliacao"] = int(avaliacao)
    _guardar_funcionarios()
    log.info(f"Funcionário {fid} atualizado com sucesso")
    return 200, f

def remover_funcionario(fid):
    log.info(f"Tentativa de remoção do funcionário: {fid}")
    _carregar_funcionarios()
    if fid not in funcionarios:
        log.error(f"Remoção falhada — funcionário não encontrado: {fid}")
        return 404, "Funcionário não encontrado"
    nome = funcionarios[fid]["nome"]
    del funcionarios[fid]
    _guardar_funcionarios()
    log.info(f"Funcionário removido com sucesso: {nome} ({fid})")
    return 200, fid