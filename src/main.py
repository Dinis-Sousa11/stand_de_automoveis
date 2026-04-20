from carros import mostrar_stock, comprar_carro
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
        code, u = cliente.fazer_login()
        if code == 200 and u:
            loading_bar("A aceder...")
            return u
        print(Fore.RED + "ID Inválido.")

    elif op == "2":
        code, msg = cliente.criar_cliente()
        print(msg)

    elif op == "0":
        print("A sair...")
        exit()

    return None


def menu_cliente(u):
    while True:
        print("\n" + Back.WHITE + Fore.BLACK + f"  LOGIN: {u['id']}  " + Style.RESET_ALL + Fore.GREEN + f"  Saldo: {int(u['saldo'])}€")
        print("1. Stock | 2. Comprar | 3. Saldo | 4. Perfil | 5. Editar | 6. Apagar | 0. Logout")
        op = input("\nComando: ").strip()

        if op == "1":
            mostrar_stock()
        elif op == "2":
            comprar_carro(u)
        elif op == "3":
            cliente.carregar_saldo(u)
        elif op == "4":
            cliente.ver_perfil(u)
        elif op == "5":
            code, msg = cliente.atualizar_cliente(u["id"])
            print(msg)
        elif op == "6":
            code, msg = cliente.remover_cliente(u["id"])
            print(msg)
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