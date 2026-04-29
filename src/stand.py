from datetime import datetime

_contador = 4

stands = {
    "S001": {"id": "S001", "nome": "Stand JDM Lisboa", "morada": "Rua do Motor, 1, Lisboa",
             "telefone": "210000001", "email": "lisboa@standjdm.pt", "nif": "500000001",
             "lista_ids_fornecedores": ["F001", "F002"], "data_registo": "2020-01-01 00:00:00"},
    "S002": {"id": "S002", "nome": "Stand JDM Porto", "morada": "Av. da Boavista, 200, Porto",
             "telefone": "220000002", "email": "porto@standjdm.pt", "nif": "500000002",
             "lista_ids_fornecedores": ["F002", "F003"], "data_registo": "2021-03-15 00:00:00"},
    "S003": {"id": "S003", "nome": "Stand JDM Faro", "morada": "Rua do Algarve, 5, Faro",
             "telefone": "289000003", "email": "faro@standjdm.pt", "nif": "500000003",
             "lista_ids_fornecedores": ["F001"], "data_registo": "2022-06-10 00:00:00"},
}

def _gerar_id():
    global _contador
    sid = f"S{_contador:03d}"
    _contador += 1
    return sid

def criar_stand(nome, morada, telefone, email, nif):
    sid = _gerar_id()
    stands[sid] = {
        "id": sid, "nome": nome, "morada": morada,
        "telefone": telefone, "email": email, "nif": nif,
        "lista_ids_fornecedores": [],
        "data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return 201, stands[sid]

def listar_stands():
    if not stands:
        return 404, "Sem stands registados"
    return 200, stands

def obter_stand(sid):
    s = stands.get(sid)
    if not s:
        return 404, "Stand não encontrado"
    return 200, s

def atualizar_stand(sid, nome=None, morada=None, telefone=None, email=None):
    s = stands.get(sid)
    if not s:
        return 404, "Stand não encontrado"
    if nome:     s["nome"] = nome
    if morada:   s["morada"] = morada
    if telefone: s["telefone"] = telefone
    if email:    s["email"] = email
    return 200, "Stand atualizado"

def remover_stand(sid):
    if sid not in stands:
        return 404, "Stand não encontrado"
    del stands[sid]
    return 200, "Stand removido"

