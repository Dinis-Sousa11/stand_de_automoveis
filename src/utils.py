import logging
from datetime import datetime

# ─── LOGGING ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    filename="logs_stand.log",
    level=logging.DEBUG,
    encoding="utf-8",
    format="%(asctime)s | %(levelname)-8s | %(module)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger(__name__)

# ─── GERADORES DE ID ────────────────────────────────────────────

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
    log.debug(f"ID gerado para '{entidade}': {novo_id}")
    return novo_id

# ─── VALIDAÇÕES ─────────────────────────────────────────────────

def validar_data(data_texto):
    try:
        datetime.strptime(data_texto, "%Y-%m-%d")
        log.debug(f"Data validada com sucesso: {data_texto}")
        return True
    except ValueError:
        log.warning(f"Formato de data inválido: '{data_texto}'")
        return False

def validar_saldo(valor):
    try:
        resultado = float(valor) > 0
        if not resultado:
            log.warning(f"Valor de saldo inválido (não positivo): {valor}")
        return resultado
    except (ValueError, TypeError):
        log.warning(f"Valor de saldo não numérico: '{valor}'")
        return False

# ─── LÓGICA DE NEGÓCIO ──────────────────────────────────────────

def fazer_login(cid):
    log.info(f"Tentativa de login com ID: {cid}")
    from cliente import clientes
    u = clientes.get(cid.upper())
    if not u:
        log.warning(f"Login falhado — ID não encontrado: {cid}")
        return 404, None
    log.info(f"Login bem-sucedido: {u['nome']} ({cid})")
    return 200, u

def carregar_saldo(u, valor):
    log.info(f"Tentativa de carregamento de saldo: cliente={u['id']}, valor={valor}€")
    if not validar_saldo(valor):
        log.warning(f"Carregamento de saldo falhado para cliente {u['id']} — valor inválido: {valor}")
        return 400, "Valor inválido"
    saldo_anterior = u["saldo"]
    u["saldo"] += float(valor)
    log.info(f"Saldo carregado: cliente={u['id']} | {saldo_anterior}€ → {u['saldo']}€ (+{float(valor)}€)")
    return 200, u["saldo"]

def comprar_carro(u, matricula):
    log.info(f"Tentativa de compra: cliente={u['id']}, matrícula={matricula}")
    from carros import carros, atualizar_carro
    carro = carros.get(matricula.upper())
    if not carro or carro["id_cliente"]:
        log.warning(f"Compra falhada — carro não disponível: {matricula}")
        return 404, "Carro não disponível"
    if u["saldo"] < carro["preco"]:
        log.warning(f"Compra falhada — saldo insuficiente: cliente={u['id']}, saldo={u['saldo']}€, preço={carro['preco']}€")
        return 403, "Saldo insuficiente"
    u["saldo"] -= carro["preco"]
    atualizar_carro(matricula.upper(), id_cliente=u["id"])
    u["carros"].append(f"{carro['marca']} {carro['modelo']}")
    log.info(f"Compra concluída: cliente={u['id']} comprou {carro['marca']} {carro['modelo']} ({matricula}) por {carro['preco']}€ | Saldo restante: {u['saldo']}€")
    return 200, "Compra efetuada"

def associar_carro_fornecedor(fid, matricula):
    log.info(f"A associar carro '{matricula}' ao fornecedor '{fid}'")
    from fornecedor import atualizar_fornecedor
    code, result = atualizar_fornecedor(fid, nova_matricula=matricula)
    if code == 200:
        log.info(f"Carro '{matricula}' associado com sucesso ao fornecedor '{fid}'")
    else:
        log.warning(f"Falha ao associar carro '{matricula}' ao fornecedor '{fid}': {result}")
    return code, result

def associar_fornecedor_stand(sid, fid):
    log.info(f"Tentativa de associação: fornecedor={fid} → stand={sid}")
    from stand import stands, atualizar_stand
    s = stands.get(sid)
    if not s:
        log.warning(f"Associação falhada — stand não encontrado: {sid}")
        return 404, "Stand não encontrado"
    if fid in s["lista_ids_fornecedores"]:
        log.warning(f"Associação falhada — fornecedor '{fid}' já está associado ao stand '{sid}'")
        return 400, "Fornecedor já associado"
    nova_lista = s["lista_ids_fornecedores"] + [fid]
    atualizar_stand(sid, lista_ids_fornecedores=nova_lista)
    log.info(f"Fornecedor '{fid}' associado com sucesso ao stand '{sid}'")
    return 200, "Fornecedor associado ao stand"