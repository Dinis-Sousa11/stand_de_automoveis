from datetime import datetime

clientes = {}

def fazer_login(cid):
    u = clientes.get(cid)
    if not u:
        return 404, None
    return 200, u

def criar_cliente(cid, nome, tel, mail):
    if cid in clientes:
        return 400, "Esse ID já existe"
    clientes[cid] = {
        "id": cid, "nome": nome, "telefone": tel, "email": mail,
        "saldo": 0.0, "carros": [],
        "data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return 200, "Conta registada com sucesso"

def carregar_saldo(u, valor):
    try:
        v = float(valor)
        if v > 0:
            u["saldo"] += v
            return 200, u["saldo"]
        return 400, "Valor inválido"
    except ValueError:
        return 403, "Número inválido"

def ver_perfil(u):
    return 200, u

def atualizar_cliente(cid, nome=None, tel=None, email=None):
    u = clientes.get(cid)
    if not u:
        return 404, "Utilizador não encontrado"
    if nome:  u["nome"] = nome
    if tel:   u["telefone"] = tel
    if email: u["email"] = email
    return 200, "Dados atualizados"

def remover_cliente(cid):
    if cid not in clientes:
        return 404, "Utilizador não encontrado"
    del clientes[cid]
    return 200, "Conta removida"
