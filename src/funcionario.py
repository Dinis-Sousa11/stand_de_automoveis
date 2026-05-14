from datetime import datetime
from utils import gerar_id
import json
import os

FICHEIRO_JSON = "funcionarios.json"


def _carregar_funcionarios():
    if os.path.exists(FICHEIRO_JSON):
        with open(FICHEIRO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return 200

def _guardar_funcionarios():
    with open(FICHEIRO_JSON, "w", encoding="utf-8") as f:
        json.dump(funcionarios, f, ensure_ascii=False, indent=2)

funcionarios = _carregar_funcionarios()


def criar_funcionario(nome, cargo, salario, telefone, turno, nif, iban, id_stand):
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
    return 201, funcionarios[fid]

def listar_funcionarios():
    if not funcionarios:
        return 404, "Sem funcionários registados"
    return 200, funcionarios

def obter_funcionario(fid):
    f = funcionarios.get(fid)
    if not f:
        return 404, "Funcionário não encontrado"
    return 200, f

def atualizar_funcionario(fid, nome=None, cargo=None, salario=None, turno=None, avaliacao=None):
    f = funcionarios.get(fid)
    if not f:
        return 404, "Funcionário não encontrado"
    if nome:      f["nome"] = nome
    if cargo:     f["cargo"] = cargo
    if salario:   f["salario"] = float(salario)
    if turno:     f["turno"] = turno
    if avaliacao: f["avaliacao"] = int(avaliacao)
    _guardar_funcionarios()
    return 200, f

def remover_funcionario(fid):
    if fid not in funcionarios:
        return 404, "Funcionário não encontrado"
    del funcionarios[fid]
    _guardar_funcionarios()
    return 200, fid