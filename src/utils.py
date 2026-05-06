from datetime import datetime

# ─── GERADORES DE ID ──────────────────────────────────────────────────────────

_contadores = {
    "cliente":      1,
    "fornecedor":   4,
    "funcionario":  4,
    "stand":        4,
    "fornecimento": 1,
}

def gerar_id(entidade):
    prefixos = {
        "cliente":      "C",
        "fornecedor":   "F",
        "funcionario":  "FN",
        "stand":        "S",
        "fornecimento": "FO",
    }
    prefixo = prefixos.get(entidade, "X")
    novo_id = f"{prefixo}{_contadores[entidade]:03d}"
    _contadores[entidade] += 1
    return novo_id

# ─── VALIDAÇÕES ───────────────────────────────────────────────────────────────

def validar_data(data_texto):
    try:
        datetime.strptime(data_texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validar_saldo(valor):
    try:
        return float(valor) > 0
    except (ValueError, TypeError):
        return False

# ─── LÓGICA DE NEGÓCIO ────────────────────────────────────────────────────────

def fazer_login(cid):
    from cliente import clientes
    u = clientes.get(cid.upper())
    if not u:
        return 404, None
    return 200, u

def carregar_saldo(u, valor):
    if not validar_saldo(valor):
        return 400, "Valor inválido"
    u["saldo"] += float(valor)
    return 200, u["saldo"]

def comprar_carro(u, matricula):
    from carros import carros
    carro = carros.get(matricula.upper())
    if not carro or carro["id_cliente"]:
        return 404, "Carro não disponível"

    if u["saldo"] < carro["preco"]:
        return 403, "Saldo insuficiente"

    u["saldo"] -= carro["preco"]
    carro["id_cliente"] = u["id"]
    u["carros"].append(f"{carro['marca']} {carro['modelo']}")
    return 200, "Compra efetuada"

def associar_carro_fornecedor(fid, matricula):
    from fornecedor import fornecedores
    f = fornecedores.get(fid)
    if not f:
        return 404, "Fornecedor não encontrado"
    f["ids_carros"].append(matricula)
    return 200, "Carro associado ao fornecedor"

def associar_fornecedor_stand(sid, fid):
    from stand import stands
    s = stands.get(sid)
    if not s:
        return 404, "Stand não encontrado"
    if fid in s["lista_ids_fornecedores"]:
        return 400, "Fornecedor já associado"
    s["lista_ids_fornecedores"].append(fid)
    return 200, "Fornecedor associado ao stand"
