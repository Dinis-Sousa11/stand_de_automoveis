from datetime import datetime

carros = [
    (("AA-00-BB", "Nissan", "Skyline R34", 1999, 85000.0, 62000, "Cinzento"), {"id_dono": None}),
    (("BB-11-CC", "Toyota", "Supra MK4", 1997, 120000.0, 45000, "Laranja"), {"id_dono": None}),
    (("CC-22-DD", "Mazda", "RX-7 FD", 1995, 55000.0, 78000, "Vermelho"), {"id_dono": None}),
    (("DD-33-EE", "Honda", "NSX", 2001, 95000.0, 33000, "Preto"), {"id_dono": None}),
    (("EE-44-FF", "Mitsubishi", "Lancer Evo IX", 2006, 45000.0, 89000, "Branco"), {"id_dono": None}),
    (("FF-55-GG", "Subaru", "Impreza 22B", 1998, 150000.0, 20000, "Azul"), {"id_dono": None}),
    (("GG-66-HH", "Nissan", "Silvia S15", 2002, 35000.0, 110000, "Amarelo"), {"id_dono": None}),
    (("HH-77-II", "Toyota", "AE86 Trueno", 1986, 30000.0, 150000, "Branco/Preto"), {"id_dono": None})
]

def criar_carro(matricula, marca, modelo, ano, preco, kms, cor):
    for c, _ in carros:
        if c[0] == matricula:
            return 400, "Já existe um carro com essa matrícula."
    dados = (matricula, marca, modelo, int(ano), float(preco), int(kms), cor)
    meta = {"data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "id_dono": None}
    carro = (dados, meta)
    carros.append(carro)
    return 201, carro

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
