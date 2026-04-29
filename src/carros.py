from datetime import datetime

carros = [
    (("AA-00-BB", "Nissan", "Skyline R34", 1999, 85000.0, 62000, "Cinzento", "RWD", 2, 2.6, 280, 4, "S001", "F001"), {"id_dono": None, "data_registo": "2024-01-10 00:00:00"}),
    (("BB-11-CC", "Toyota", "Supra MK4", 1997, 120000.0, 45000, "Laranja", "RWD", 2, 3.0, 320, 4, "S001", "F001"), {"id_dono": None, "data_registo": "2024-01-12 00:00:00"}),
    (("CC-22-DD", "Mazda", "RX-7 FD", 1995, 55000.0, 78000, "Vermelho", "RWD", 2, 1.3, 255, 4, "S002", "F002"), {"id_dono": None, "data_registo": "2024-02-01 00:00:00"}),
    (("DD-33-EE", "Honda", "NSX", 2001, 95000.0, 33000, "Preto", "RWD", 2, 3.2, 290, 2, "S002", "F002"), {"id_dono": None, "data_registo": "2024-02-15 00:00:00"}),
    (("EE-44-FF", "Mitsubishi", "Lancer Evo IX", 2006, 45000.0, 89000, "Branco", "4WD", 4, 2.0, 280, 5, "S001", "F003"), {"id_dono": None, "data_registo": "2024-03-01 00:00:00"}),
    (("FF-55-GG", "Subaru", "Impreza 22B", 1998, 150000.0, 20000, "Azul", "4WD", 2, 2.0, 280, 4, "S003", "F001"), {"id_dono": None, "data_registo": "2024-03-10 00:00:00"}),
    (("GG-66-HH", "Nissan", "Silvia S15", 2002, 35000.0, 110000, "Amarelo", "RWD", 2, 2.0, 200, 4, "S003", "F002"), {"id_dono": None, "data_registo": "2024-04-01 00:00:00"}),
    (("HH-77-II", "Toyota", "AE86 Trueno", 1986, 30000.0, 150000, "Branco", "RWD", 2, 1.6, 128, 4, "S002", "F003"), {"id_dono": None, "data_registo": "2024-04-05 00:00:00"}),
]


def criar_carro(matricula, marca, modelo, ano, preco, kms, cor,
                tracao, num_portas, cilindrada, potencia, lotacao, id_stand, id_fornecedor):
    for c, _ in carros:
        if c[0] == matricula:
            return 400, "Já existe um carro com essa matrícula."
    dados = (matricula, marca, modelo, int(ano), float(preco), int(kms), cor,
             tracao, int(num_portas), float(cilindrada), int(potencia), int(lotacao),
             id_stand, id_fornecedor)
    meta = {"id_dono": None, "data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    carros.append((dados, meta))
    return 201, (dados, meta)

def obter_carro(matricula):
    for dados, meta in carros:
        if dados[0] == matricula.upper():
            return 200, dados, meta
    return 404, "Não encontrado", None

def listar_stock():
    disponiveis = [(d, m) for d, m in carros if not m["id_dono"]]
    if not disponiveis:
        return 404, []
    return 200, disponiveis

def atualizar_carro(matricula, marca=None, modelo=None, ano=None, preco=None, kms=None, cor=None):
    for i, (dados, meta) in enumerate(carros):
        if dados[0] == matricula.upper():
            d = list(dados)
            if marca:  d[1] = marca
            if modelo: d[2] = modelo
            if ano:    d[3] = ano
            if preco:  d[4] = preco
            if kms:    d[5] = kms
            if cor:    d[6] = cor
            carros[i] = (tuple(d), meta)
            return 200, carros[i]
    return 404, "Carro não encontrado"

def remover_carro(matricula):
    for i, (dados, meta) in enumerate(carros):
        if dados[0] == matricula.upper():
            if meta["id_dono"]:
                return 400, "Carro já tem dono"
            carros.pop(i)
            return 200, "Carro removido"
    return 404, "Carro não encontrado"

def comprar_carro(u, matricula):
    carro = next(((d, m) for d, m in carros if d[0] == matricula and not m["id_dono"]), None)
    if not carro:
        return 404, "Carro não disponível"
    if u["saldo"] < carro[0][4]:
        return 403, "Saldo insuficiente"
    u["saldo"] -= carro[0][4]
    carro[1]["id_dono"] = u["id"]
    u["carros"].append(f"{carro[0][1]} {carro[0][2]}")
    return 200, "Compra efetuada"
