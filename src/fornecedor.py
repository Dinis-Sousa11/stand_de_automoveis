from datetime import datetime
from utils import gerar_id

fornecedores = {
    "F001": {"id": "F001", "nome": "Tokyo Auto Import", "contacto": "+81 3-0000-0001", "pais": "Japão", "email": "contact@tokyoauto.jp", "tipo": "importador", "morada": "1-1 Shibuya, Tokyo", "avaliacao": 5, "ids_carros": [], "data_registo": "2020-01-01 00:00:00"},
    "F002": {"id": "F002", "nome": "JDM Auctions Ltd", "contacto": "+81 6-0000-0002", "pais": "Japão", "email": "info@jdmauctions.jp", "tipo": "leiloeiro", "morada": "2-5 Osaka Namba", "avaliacao": 4, "ids_carros": [], "data_registo": "2020-06-01 00:00:00"},
    "F003": {"id": "F003", "nome": "Euro JDM Motors", "contacto": "+44 20 0000 0003", "pais": "Reino Unido", "email": "sales@eurojdm.co.uk", "tipo": "importador", "morada": "10 Car Street, London", "avaliacao": 4, "ids_carros": [], "data_registo": "2021-01-10 00:00:00"},
}

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

def atualizar_fornecedor(fid, nome=None, contacto=None, avaliacao=None, morada=None):
    f = fornecedores.get(fid)
    if not f:
        return 404, "Fornecedor não encontrado"
    if nome:      f["nome"] = nome
    if contacto:  f["contacto"] = contacto
    if avaliacao: f["avaliacao"] = int(avaliacao)
    if morada:    f["morada"] = morada
    return 200, f

def remover_fornecedor(fid):
    if fid not in fornecedores:
        return 404, "Fornecedor não encontrado"
    del fornecedores[fid]
    return 200, fid
