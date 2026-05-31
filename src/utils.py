import logging
import os
from datetime import datetime


# ─── CONFIGURAÇÃO DO LOGGING ─────────────────────────────────────────────

def configurar_logging(
        nome_arquivo: str = "logs_stand.log",
        nivel: int = logging.DEBUG,
        criar_pasta: bool = True
) -> logging.Logger:
    """Configura e retorna o logger principal."""
    if criar_pasta:
        os.makedirs("logs", exist_ok=True)
        caminho = os.path.join("logs", nome_arquivo)
    else:
        caminho = nome_arquivo

    logging.basicConfig(
        filename=caminho,
        level=nivel,
        encoding="utf-8",
        format="%(asctime)s | %(levelname)-8s | %(module)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True
    )

    logger = logging.getLogger(__name__)
    logger.info(f"✅ Logging configurado → {caminho}")
    return logger


# Configuração inicial (executada quando o módulo é importado)
log = configurar_logging()

# ─── GERADORES DE ID ─────────────────────────────────────────────────────

_contadores = {
    "cliente": 1,
    "fornecedor": 4,
    "funcionario": 4,
    "stand": 4,
    "fornecimento": 1,
}


def gerar_id(entidade: str) -> str:
    prefixos = {
        "cliente": "C",
        "fornecedor": "F",
        "funcionario": "FN",
        "stand": "S",
        "fornecimento": "FO",
    }

    if entidade not in _contadores:
        log.error(f"Entidade desconhecida: {entidade}")
        raise ValueError(f"Entidade desconhecida: {entidade}")

    prefixo = prefixos.get(entidade, "X")
    novo_id = f"{prefixo}{_contadores[entidade]:03d}"
    _contadores[entidade] += 1

    log.debug(f"ID gerado para '{entidade}': {novo_id}")
    return novo_id


# ─── VALIDAÇÕES ──────────────────────────────────────────────────────────

def validar_data(data_texto: str) -> bool:
    try:
        datetime.strptime(data_texto, "%Y-%m-%d")
        log.debug(f"Data validada: {data_texto}")
        return True
    except ValueError:
        log.exception(f"Formato de data inválido: '{data_texto}'")
        return False


def validar_saldo(valor) -> bool:
    try:
        resultado = float(valor) > 0
        if not resultado:
            log.error(f"Valor de saldo inválido (não positivo): {valor}")
        return resultado
    except (ValueError, TypeError):
        log.exception(f"Valor de saldo não numérico: '{valor}'")
        return False


# ─── LÓGICA DE NEGÓCIO ───────────────────────────────────────────────────

def fazer_login(cid: str):
    log.info(f"Tentativa de login com ID: {cid}")
    try:
        from cliente import clientes  # import dentro da função evita circular import
        u = clientes.get(cid.upper())

        if not u:
            log.error(f"Login falhado — ID não encontrado: {cid}")
            return 404, None

        log.info(f"Login bem-sucedido: {u.get('nome')} ({cid})")
        return 200, u
    except Exception as e:
        log.exception("Erro inesperado durante o login")
        return 500, None


def carregar_saldo(u: dict, valor):
    log.info(f"Tentativa de carregamento de saldo: cliente={u.get('id')}, valor={valor}€")

    if not validar_saldo(valor):
        return 400, "Valor inválido"

    saldo_anterior = u["saldo"]
    u["saldo"] += float(valor)

    log.info(f"Saldo carregado: {u.get('id')} | {saldo_anterior}€ → {u['saldo']}€")
    return 200, u["saldo"]