from datetime import datetime

# Lista inicial de carros (Dados do carro, Metadados)
carros = [
    (("AA-00-BB", "Nissan", "Skyline R34", 1999, 85000.0, 62000, "Cinzento"), {"data_registo": "2024-01-01 10:00:00", "id_dono": None}),
    (("BB-11-CC", "Toyota", "Supra MK4", 1997, 120000.0, 45000, "Laranja"), {"data_registo": "2024-01-01 10:00:00", "id_dono": None}),
    (("CC-22-DD", "Mazda", "RX-7 FD", 1995, 55000.0, 78000, "Vermelho"), {"data_registo": "2024-01-01 10:00:00", "id_dono": None}),
    (("DD-33-EE", "Honda", "NSX", 2001, 95000.0, 33000, "Preto"), {"data_registo": "2024-01-01 10:00:00", "id_dono": None}),
    (("EE-44-FF", "Mitsubishi", "Lancer Evo VI", 1999, 42000.0, 91000, "Branco"), {"data_registo": "2024-01-01 10:00:00", "id_dono": None}),
    (("FF-55-GG", "Subaru", "Impreza WRX STI", 2003, 38000.0, 105000, "Azul"), {"data_registo": "2024-01-01 10:00:00", "id_dono": None}),
    (("GG-66-HH", "Honda", "Civic Type R EK9", 1998, 28000.0, 87000, "Vermelho"), {"data_registo": "2024-01-01 10:00:00", "id_dono": None}),
    (("HH-77-II", "Toyota", "AE86 Trueno", 1985, 32000.0, 120000, "Preto/Branco"), {"data_registo": "2024-01-01 10:00:00", "id_dono": None})
]


# CREATE
def criar_carro(matricula, marca, modelo, ano, preco, kms, cor):
    for c, _ in carros:
        if c[0] == matricula:
            print("Ja existe um carro com essa matricula.")
            return None
    dados = (matricula, marca, modelo, int(ano), float(preco), int(kms), cor)
    meta = {"data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "id_dono": None}
    carros.append((dados, meta))
    return matricula


# READ (auxiliar)
def obter_carro(matricula):
    for dados, meta in carros:
        if dados[0] == matricula.upper():
            return dados, meta
    return None


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
            return True
    return False


# DELETE
def remover_carro(matricula):
    for i, (dados, meta) in enumerate(carros):
        if dados[0] == matricula.upper():
            if meta["id_dono"]:
                print("Erro: carro ja tem dono, nao pode ser removido.")
                return False
            carros.pop(i)
            return True
    return False


# Associar dono (usado na compra)
def associar_dono(matricula, id_cliente):
    for dados, meta in carros:
        if dados[0] == matricula.upper():
            meta["id_dono"] = id_cliente
            return True
    return False