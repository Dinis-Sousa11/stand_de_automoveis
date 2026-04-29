
contador_ids = 1

def gerar_id_cliente():
    global contador_ids
    novo_id = f"C{contador_ids:03d}"
    contador_ids += 1
    return novo_id

def validar_saldo(valor):
    try:
        v = float(valor)
        return v > 0
    except (ValueError, TypeError):
        return False


