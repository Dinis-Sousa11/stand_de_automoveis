
from datetime import datetime
from colorama import Fore, Style

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


# CREATE
def criar_carro(matricula, marca, modelo, ano, preco, kms, cor):
    for c, _ in carros:
        if c[0] == matricula:
            return 400, "Já existe um carro com essa matrícula."
    dados = (matricula, marca, modelo, int(ano), float(preco), int(kms), cor)
    meta = {"data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "id_dono": None}
    carro = (dados, meta)
    carros.append(carro)
    return 201, carro


# READ (individual)
def obter_carro(matricula):
    for dados, meta in carros:
        if dados[0] == matricula.upper():
            return 200, dados, meta
    return 404, "Não foi encontrado", None


# UPDATE
def atualizar_carro(matricula, **kwargs):
    for i, (dados, meta) in enumerate(carros):
        if dados[0] == matricula.upper():
            d = list(dados)
            campos = ["matricula", "marca", "modelo", "ano", "preco", "kms", "cor"]
            for chave, valor in kwargs.items():
                if chave in campos:
                    d[campos.index(chave)] = valor
            carros[i] = (tuple(d), meta)
            return 200, carros[i]
    return 404, "Carro não encontrado"


# DELETE
def remover_carro(matricula):
    for i, (dados, meta) in enumerate(carros):
        if dados[0] == matricula.upper():
            if meta["id_dono"]:
                return 400, "Carro já tem dono"
            carros.pop(i)
            return 200, "Carro removido"
    return 404, "Carro não encontrado"


# associar dono (usado na compra)
def associar_dono(matricula, id_cliente):
    for dados, meta in carros:
        if dados[0] == matricula.upper():
            meta["id_dono"] = id_cliente
            return 200, "Dono associado"
    return 404, "Carro não encontrado"


# READ (stock - UI)
def mostrar_stock():
    print(f"\n{Fore.CYAN}{'=' * 45}")
    print(f"{Fore.WHITE}{Style.BRIGHT}         INVENTÁRIO STAND JDM")
    print(f"{Fore.CYAN}{'=' * 45}")
    for d, m in carros:
        if not m["id_dono"]:
            print(f"{Fore.YELLOW}{d[0]}{Fore.WHITE} | {d[1]} {d[2]:<15} | {Fore.GREEN}{int(d[4])}€")
    input("\nEnter para continuar...")


# compra
def comprar_carro(u):
    mat = input("\nDigite a matrícula: ").strip().upper()
    carro = next(((d, m) for d, m in carros if d[0] == mat and not m["id_dono"]), None)

    if not carro:
        print(Fore.RED + "Carro não disponível.")
        return 404, "Carro não disponível"

    if u["saldo"] < carro[0][4]:
        print(Fore.RED + "Saldo insuficiente.")
        return 403, "Saldo insuficiente"

    u["saldo"] -= carro[0][4]
    carro[1]["id_dono"] = u["id"]
    u["carros"].append(f"{carro[0][1]} {carro[0][2]}")
    print(Fore.GREEN + "Compra efetuada!")
    return 200, "Compra efetuada"