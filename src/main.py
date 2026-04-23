from carros import listar_stock, comprar_carro
import cliente
import time
import sys
from colorama import Fore, Back, Style, init

init(autoreset=True)

def loading_bar(texto):
    print(Fore.WHITE + texto, end="")
    for _ in range(15):
        time.sleep(0.03)
        sys.stdout.write(Fore.GREEN + "█")
        sys.stdout.flush()
    print(" OK!")

def login():
    print(f"\n{Fore.MAGENTA}===================================")
    print(f"{Fore.WHITE}{Style.BRIGHT}      STAND JDM - LOGIN")
    print(f"{Fore.MAGENTA}===================================")
    print("1. Entrar | 2. Novo Registo | 0. Sair")
    op = input("\nEscolha: ").strip()

    if op == "1":
        cid = input("ID de cliente: ").upper().strip()
        code, u = cliente.fazer_login(cid)
        if code == 200:
            loading_bar("A aceder...")
            return u
        print(Fore.RED + "ID Inválido.")

    elif op == "2":
        print(f"\n{Fore.YELLOW}--- NOVO REGISTO ---")
        cid  = input("ID (Login): ").upper().strip()
        nome = input("Nome: ")
        tel  = input("Telefone: ")
        mail = input("Email: ")
        code, msg = cliente.criar_cliente(cid, nome, tel, mail)
        print(Fore.GREEN + msg if code == 200 else Fore.RED + msg)

    elif op == "0":
        exit()

    return None

def menu_cliente(u):
    while True:
        print("\n" + Back.WHITE + Fore.BLACK + f"  LOGIN: {u['id']}  " + Style.RESET_ALL + Fore.GREEN + f"  Saldo: {int(u['saldo'])}€")
        print("1. Stock | 2. Comprar | 3. Saldo | 4. Perfil | 5. Editar | 6. Apagar | 0. Logout")
        op = input("\nComando: ").strip()

        if op == "1":
            code, stock = listar_stock()
            if code == 200:
                print(f"\n{Fore.CYAN}{'=' * 45}")
                print(f"{Fore.WHITE}{Style.BRIGHT}         INVENTÁRIO STAND JDM")
                print(f"{Fore.CYAN}{'=' * 45}")
                for d, _ in stock:
                    print(f"{Fore.YELLOW}{d[0]}{Fore.WHITE} | {d[1]} {d[2]:<15} | {Fore.GREEN}{int(d[4])}€")
            else:
                print(Fore.RED + "Sem stock disponível.")
            input("\nEnter para continuar...")

        elif op == "2":
            mat = input("\nDigite a matrícula: ").strip().upper()
            code, msg = comprar_carro(u, mat)
            print(Fore.GREEN + msg if code == 200 else Fore.RED + msg)

        elif op == "3":
            valor = input("\nValor a depositar (€): ")
            code, msg = cliente.carregar_saldo(u, valor)
            print(Fore.GREEN + str(msg) if code == 200 else Fore.RED + str(msg))

        elif op == "4":
            code, obj = cliente.ver_perfil(u)
            print(f"\n{Fore.YELLOW}--- O TEU PERFIL ---")
            print(f"ID: {obj['id']} | Nome: {obj['nome']}")
            print(f"Contacto: {obj['telefone']} | Email: {obj['email']}")
            print(f"Membro desde: {obj['data_registo']}")
            print(f"Garagem: {Fore.CYAN}{', '.join(obj['carros']) if obj['carros'] else 'Vazia'}")
            input("\nEnter para voltar...")

        elif op == "5":
            print(f"\n{Fore.YELLOW}--- EDITAR PERFIL (Vazio para manter) ---")
            n = input(f"Novo Nome [{u['nome']}]: ").strip()
            t = input(f"Novo Tel [{u['telefone']}]: ").strip()
            e = input(f"Novo Email [{u['email']}]: ").strip()
            code, msg = cliente.atualizar_cliente(u["id"], n or None, t or None, e or None)
            print(Fore.BLUE + msg if code == 200 else Fore.RED + msg)

        elif op == "6":
            confirma = input(Fore.RED + "Tens a certeza que queres APAGAR a conta? (s/n): ").lower()
            if confirma == 's':
                code, msg = cliente.remover_cliente(u["id"])
                print(Fore.RED + msg if code == 200 else Fore.RED + msg)
                if code == 200:
                    break

        elif op == "0":
            break

def main():
    while True:
        u = login()
        if u:
            menu_cliente(u)

if __name__ == "__main__":
    main()
