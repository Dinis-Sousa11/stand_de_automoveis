from datetime import datetime

clientes = {}


# CREATE
def criar_cliente(cid, nome, telefone, email, tipo="particular"):
    cid = cid.upper()
    if cid in clientes:
        print("Erro: Esse ID ja esta em uso.")
        return None

    for c in clientes.values():
        if c["email"] == email:
            print("Erro: Email ja registado.")
            return None

    clientes[cid] = {
        "id": cid,
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "tipo": tipo,
        "saldo": 0.0,
        "data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "carros": []
    }
    return cid


# UPDATE
def atualizar_cliente(cid, **kwargs):
    c = clientes.get(cid.upper())
    if not c:
        return False
    campos_permitidos = ["nome", "telefone", "email", "tipo"]
    for chave, valor in kwargs.items():
        if chave in campos_permitidos:
            c[chave] = valor
    return True


# DELETE
def remover_cliente(cid):
    cid = cid.upper()
    if cid not in clientes:
        return False
    clientes.pop(cid)
    return True


# Adicionar carro ao cliente (usado na compra)
def adicionar_carro(cid, matricula):
    c = clientes.get(cid.upper())
    if c:
        c["carros"].append(matricula)
