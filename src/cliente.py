from datetime import datetime

clientes = {}
_contador = 1

def _gerar_id():
    global _contador
    cid = f"C{_contador:03d}"
    _contador += 1
    return cid

def criar_cliente(nome, data_nascimento, telefone, email, preferencias, tipo_compra):
    cid = _gerar_id()
    clientes[cid] = {
        "id": cid, "nome": nome, "data_nascimento": data_nascimento,
        "telefone": telefone, "email": email,
        "preferencias": preferencias, "tipo_compra": tipo_compra,
        "saldo": 0.0, "carros": [],
        "data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return 201, clientes[cid]

def fazer_login(cid):
    u = clientes.get(cid.upper())
    if not u:
        return 404, None
    return 200, u

def ver_perfil(u):
    return 200, u

def carregar_saldo(u, valor):
    try:
        v = float(valor)
        if v > 0:
            u["saldo"] += v
            return 200, u["saldo"]
        return 400, "Valor inválido"
    except ValueError:
        return 403, "Número inválido"

def atualizar_cliente(cid, nome=None, telefone=None, email=None, preferencias=None, tipo_compra=None):
    u = clientes.get(cid)
    if not u:
        return 404, "Cliente não encontrado"
    if nome:         u["nome"] = nome
    if telefone:     u["telefone"] = telefone
    if email:        u["email"] = email
    if preferencias: u["preferencias"] = preferencias
    if tipo_compra:  u["tipo_compra"] = tipo_compra
    return 200, "Dados atualizados"

def remover_cliente(cid):
    if cid not in clientes:
        return 404, "Cliente não encontrado"
    del clientes[cid]
    return 200, "Conta removida"