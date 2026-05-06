from datetime import datetime

fornecimentos = {}
_contador = 1

def _gerar_id():
    global _contador
    fid = f"FO{_contador:03d}"
    _contador += 1
    return fid

# CREATE
def criar_fornecimento(id_stand, id_fornecedor):
    for fo in fornecimentos.values():
        if fo["id_stand"] == id_stand and fo["id_fornecedor"] == id_fornecedor:
            return 400, "Fornecimento já existe"
    foid = _gerar_id()
    fornecimentos[foid] = {
        "id": foid,
        "id_stand": id_stand,
        "id_fornecedor": id_fornecedor,
        "data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return 201, fornecimentos[foid]

# READ
def listar_fornecimentos():
    if not fornecimentos:
        return 404, "Sem fornecimentos registados"
    return 200, fornecimentos

def obter_fornecimento(foid):
    fo = fornecimentos.get(foid)
    if not fo:
        return 404, "Fornecimento não encontrado"
    return 200, fo

# DELETE
def remover_fornecimento(foid):
    if foid not in fornecimentos:
        return 404, "Fornecimento não encontrado"
    del fornecimentos[foid]
    return 200, "Fornecimento removido"
