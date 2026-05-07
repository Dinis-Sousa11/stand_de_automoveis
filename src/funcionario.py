from datetime import datetime
from utils import gerar_id

funcionarios = {
    "FN001": {"id": "FN001", "nome": "Carlos Silva", "cargo": "Vendedor", "salario": 1200.0, "telefone": "910000001", "turno": "manhã", "nif": "123456789", "iban": "PT50000201231234567890154", "id_stand": "S001", "avaliacao": 4, "vendas_realizadas": [], "data_entrada": "2020-02-01 00:00:00"},
    "FN002": {"id": "FN002", "nome": "Ana Ferreira", "cargo": "Gestora", "salario": 1800.0, "telefone": "920000002", "turno": "manhã", "nif": "987654321", "iban": "PT50000201231234567890155", "id_stand": "S001", "avaliacao": 5, "vendas_realizadas": [], "data_entrada": "2019-05-10 00:00:00"},
    "FN003": {"id": "FN003", "nome": "Rui Costa", "cargo": "Mecânico", "salario": 1100.0, "telefone": "930000003", "turno": "tarde", "nif": "112233445", "iban": "PT50000201231234567890156", "id_stand": "S002", "avaliacao": 3, "vendas_realizadas": [], "data_entrada": "2021-09-20 00:00:00"},
}

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
    return 200, f

def remover_funcionario(fid):
    if fid not in funcionarios:
        return 404, "Funcionário não encontrado"
    del funcionarios[fid]
    return 200, fid
