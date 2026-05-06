from datetime import datetime
from utils import gerar_id

carros = {
    "AA-00-BB": {"matricula": "AA-00-BB", "marca": "Nissan", "modelo": "Skyline R34", "ano": 1999, "preco": 85000.0, "kms": 62000, "cor": "Cinzento", "tracao": "RWD", "num_portas": 2, "cilindrada": 2.6, "potencia": 280, "lotacao": 4, "id_stand": "S001", "id_fornecedor": "F001", "id_cliente": None, "data_registo": "2024-01-10 00:00:00"},
    "BB-11-CC": {"matricula": "BB-11-CC", "marca": "Toyota", "modelo": "Supra MK4", "ano": 1997, "preco": 120000.0, "kms": 45000, "cor": "Laranja", "tracao": "RWD", "num_portas": 2, "cilindrada": 3.0, "potencia": 320, "lotacao": 4, "id_stand": "S001", "id_fornecedor": "F001", "id_cliente": None, "data_registo": "2024-01-12 00:00:00"},
    "CC-22-DD": {"matricula": "CC-22-DD", "marca": "Mazda", "modelo": "RX-7 FD", "ano": 1995, "preco": 55000.0, "kms": 78000, "cor": "Vermelho", "tracao": "RWD", "num_portas": 2, "cilindrada": 1.3, "potencia": 255, "lotacao": 4, "id_stand": "S002", "id_fornecedor": "F002", "id_cliente": None, "data_registo": "2024-02-01 00:00:00"},
    "DD-33-EE": {"matricula": "DD-33-EE", "marca": "Honda", "modelo": "NSX", "ano": 2001, "preco": 95000.0, "kms": 33000, "cor": "Preto", "tracao": "RWD", "num_portas": 2, "cilindrada": 3.2, "potencia": 290, "lotacao": 2, "id_stand": "S002", "id_fornecedor": "F002", "id_cliente": None, "data_registo": "2024-02-15 00:00:00"},
    "EE-44-FF": {"matricula": "EE-44-FF", "marca": "Mitsubishi", "modelo": "Lancer Evo IX", "ano": 2006, "preco": 45000.0, "kms": 89000, "cor": "Branco", "tracao": "4WD", "num_portas": 4, "cilindrada": 2.0, "potencia": 280, "lotacao": 5, "id_stand": "S001", "id_fornecedor": "F003", "id_cliente": None, "data_registo": "2024-03-01 00:00:00"},
    "FF-55-GG": {"matricula": "FF-55-GG", "marca": "Subaru", "modelo": "Impreza 22B", "ano": 1998, "preco": 150000.0, "kms": 20000, "cor": "Azul", "tracao": "4WD", "num_portas": 2, "cilindrada": 2.0, "potencia": 280, "lotacao": 4, "id_stand": "S003", "id_fornecedor": "F001", "id_cliente": None, "data_registo": "2024-03-10 00:00:00"},
    "GG-66-HH": {"matricula": "GG-66-HH", "marca": "Nissan", "modelo": "Silvia S15", "ano": 2002, "preco": 35000.0, "kms": 110000, "cor": "Amarelo", "tracao": "RWD", "num_portas": 2, "cilindrada": 2.0, "potencia": 200, "lotacao": 4, "id_stand": "S003", "id_fornecedor": "F002", "id_cliente": None, "data_registo": "2024-04-01 00:00:00"},
    "HH-77-II": {"matricula": "HH-77-II", "marca": "Toyota", "modelo": "AE86 Trueno", "ano": 1986, "preco": 30000.0, "kms": 150000, "cor": "Branco", "tracao": "RWD", "num_portas": 2, "cilindrada": 1.6, "potencia": 128, "lotacao": 4, "id_stand": "S002", "id_fornecedor": "F003", "id_cliente": None, "data_registo": "2024-04-05 00:00:00"},
}

def criar_carro(matricula, marca, modelo, ano, preco, kms, cor,
                tracao, num_portas, cilindrada, potencia, lotacao, id_stand, id_fornecedor):
    if matricula in carros:
        return 400, "Já existe um carro com essa matrícula."
    carro = {
        "matricula": matricula,
        "marca": marca,
        "modelo": modelo,
        "ano": int(ano),
        "preco": float(preco), "kms": int(kms),
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
    return 201, carro

def listar_stock():
    disponiveis = {m: c for m, c in carros.items() if not c["id_cliente"]}
    if not disponiveis:
        return 404, {}
    return 200, disponiveis

def obter_carro(matricula):
    carro = carros.get(matricula.upper())
    if not carro:
        return 404, "Não encontrado"
    return 200, carro

def atualizar_carro(matricula, marca=None, modelo=None, ano=None, preco=None, kms=None, cor=None):
    carro = carros.get(matricula.upper())
    if not carro:
        return 404, "Carro não encontrado"
    if marca:  carro["marca"] = marca
    if modelo: carro["modelo"] = modelo
    if ano:    carro["ano"] = ano
    if preco:  carro["preco"] = preco
    if kms:    carro["kms"] = kms
    if cor:    carro["cor"] = cor
    return 200, carro

def remover_carro(matricula):
    carro = carros.get(matricula.upper())
    if not carro:
        return 404, "Carro não encontrado"
    if carro["id_cliente"]:
        return 400, "Carro já tem dono"
    del carros[matricula.upper()]
    return 200, matricula
