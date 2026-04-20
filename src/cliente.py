
from datetime import datetime
from colorama import Fore

clientes = {}


# CREATE
def criar_cliente():
    print(f"\n{Fore.YELLOW}--- NOVO REGISTO ---")
    cid = input("ID (Login): ").upper().strip()

    if cid in clientes:
        return 400, Fore.RED + "Esse ID já existe"

    nome = input("Nome: ")
    tel = input("Telefone: ")
    mail = input("Email: ")

    clientes[cid] = {
        "id": cid,
        "nome": nome,
        "telefone": tel,
        "email": mail,
        "saldo": 0.0,
        "carros": [],
        "data_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return 200, Fore.GREEN + "Conta registada com sucesso"


# READ (login)
def fazer_login():
    cid = input("ID de cliente: ").upper().strip()
    u = clientes.get(cid)
    if not u:
        return 404, None
    return 200, u


# UPDATE (saldo)
def carregar_saldo(u):
    try:
        v = float(input("\nValor a depositar (€): "))
        if v > 0:
            u["saldo"] += v
            print(Fore.GREEN + "Saldo atualizado!")
            return 200, u["saldo"]
        else:
            print(Fore.RED + "O valor deve ser positivo.")
            return 400, "Valor inválido"
    except ValueError:
        print(Fore.RED + "Erro: Digite um número válido.")
        return 403, "Número inválido"


# READ (perfil)
def ver_perfil(u):
    print(f"\n{Fore.YELLOW}--- O TEU PERFIL ---")
    print(f"ID: {u['id']} | Nome: {u['nome']}")
    print(f"Contacto: {u['telefone']} | Email: {u['email']}")
    print(f"Membro desde: {u['data_registo']}")
    print(f"Garagem: {Fore.CYAN}{', '.join(u['carros']) if u['carros'] else 'Vazia'}")
    input("\nEnter para voltar...")
    return 200, u


# UPDATE (dados)
def atualizar_cliente(cid):
    u = clientes.get(cid)
    if not u:
        return 404, Fore.RED + "Utilizador não encontrado"

    print(f"\n{Fore.YELLOW}--- EDITAR PERFIL (Vazio para manter) ---")
    n = input(f"Novo Nome [{u['nome']}]: ").strip()
    t = input(f"Novo Tel [{u['telefone']}]: ").strip()
    e = input(f"Novo Email [{u['email']}]: ").strip()

    if n: u["nome"] = n
    if t: u["telefone"] = t
    if e: u["email"] = e
    return 200, Fore.BLUE + "Dados atualizados"


# DELETE
def remover_cliente(cid):
    confirma = input(Fore.RED + "Tens a certeza que queres APAGAR a conta? (s/n): ").lower()
    if confirma == 's':
        if cid in clientes:
            del clientes[cid]
            return 200, Fore.RED + "Conta removida com sucesso"
        return 404, "Utilizador não encontrado"
    return 403, "Operação cancelada"