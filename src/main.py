import carros
import utilizador
import time
import sys
from colorama import Fore, Back, Style, init

init(autoreset=True)


def loading_bar(texto):
    print(Fore.WHITE + texto, end="")
    for _ in range(20):
        time.sleep(0.05)
        sys.stdout.write(Fore.GREEN + "█")
        sys.stdout.flush()
    print(Style.RESET_ALL + " OK!")


# --- LÓGICA DO PROGRAMA ---

def login():
    print("\n" + Fore.MAGENTA + "=" * 35)
    print(Fore.WHITE + Style.BRIGHT + "      Stand de Automóveis JDM")
    print(Fore.MAGENTA + "=" * 35)
    print(f"{Fore.CYAN}1.{Fore.WHITE} Entrar na Garagem")
    print(f"{Fore.CYAN}2.{Fore.WHITE} Novo Registo")
    print(f"{Fore.RED}0.{Fore.WHITE} Sair")

    op = input("\nEscolha: ").strip()

    if op == "1":
        cid = input("ID de utilizador: ").strip().upper()
        c = utilizador.clientes.get(cid)
        if c:
            loading_bar("A aceder ao servidor... ")
            print(Fore.GREEN + f"\nBem-vindo de volta, {c['nome']}!")
            return c
        print(Fore.RED + "ID Inválido.")

    elif op == "2":
        novo_id = input("Escolha o seu ID: ").strip().upper()
        nome = input("Nome: ").strip()
        tel = input("Telefone: ").strip()
        email = input("Email: ").strip()
        print(f"{Fore.CYAN}1. Particular | 2. Empresa")
        tipo = "empresa" if input("Tipo: ") == "2" else "particular"

        if utilizador.criar_cliente(novo_id, nome, tel, email, tipo):
            print(Fore.GREEN + "Conta registada! Faz login agora.")
    return None


def menu_cliente(cliente):
    while True:
        print("\n" + Back.WHITE + Fore.BLACK + f"  LOGGED AS: {cliente['id']}  " + Style.RESET_ALL +
              Fore.GREEN + f"  Saldo: {int(cliente['saldo'])}€")
        print(f"{Fore.CYAN}1.{Fore.WHITE} Ver Stock")
        print(f"{Fore.CYAN}2.{Fore.WHITE} Comprar Carro")
        print(f"{Fore.CYAN}3.{Fore.WHITE} Carregar Saldo")
        print(f"{Fore.CYAN}4.{Fore.WHITE} Perfil")
        print(f"{Fore.CYAN}5.{Fore.WHITE} Editar Perfil")
        print(f"{Fore.CYAN}6.{Fore.WHITE} Apagar Conta")
        print(f"{Fore.RED}0.{Fore.WHITE} Logout")

        op = input("\nComando: ").strip()

        if op == "1":
            disponiveis = [(d, m) for d, m in carros.carros if not m["id_dono"]]
            for d, m in disponiveis:
                print(f"{Fore.CYAN}{d[0]}{Fore.WHITE} | {d[1]} {d[2]} | {Fore.GREEN}{int(d[4])}€")
            input("\nPressione Enter para continuar...")

        elif op == "2":
            mat = input("Matrícula do carro: ").strip().upper()
            carro = next(((d, m) for d, m in carros.carros if d[0] == mat and not m["id_dono"]), None)

            if not carro:
                print(Fore.RED + "Carro não disponível.")
            elif cliente["saldo"] < carro[0][4]:
                print(Back.RED + " SALDO INSUFICIENTE ")
            else:
                loading_bar("A processar pagamento... ")
                cliente["saldo"] -= carro[0][4]
                carros.associar_dono(mat, cliente["id"])
                utilizador.adicionar_carro(cliente["id"], mat)
                print(Fore.GREEN + Style.BRIGHT + f"\nPARABÉNS! O {carro[0][2]} é teu!")

        elif op == "3":
            try:
                v = float(input("Valor (€): "))
                cliente["saldo"] += v
                loading_bar("A depositar... ")
            except:
                print(Fore.RED + "Erro.")

        elif op == "4":
            print(f"\n{Fore.YELLOW}ID: {cliente['id']} | Nome: {cliente['nome']}")
            print(f"carros: {Fore.CYAN}{', '.join(cliente['carros'])}")
            input("\nEnter para voltar...")

        elif op == "5":
            print(Fore.YELLOW + "Deixa vazio para não alterar.")
            nome = input("Novo nome: ").strip()
            tel = input("Novo telefone: ").strip()
            email = input("Novo email: ").strip()
            kwargs = {}
            if nome: kwargs["nome"] = nome
            if tel: kwargs["telefone"] = tel
            if email: kwargs["email"] = email
            if kwargs and utilizador.atualizar_cliente(cliente["id"], **kwargs):
                cliente.update(kwargs)
                print(Fore.GREEN + "Perfil atualizado!")
            else:
                print(Fore.YELLOW + "Nenhuma alteração feita.")

        elif op == "6":
            conf = input(Fore.RED + "Tens a certeza? (s/n): ").strip().lower()
            if conf == "s":
                utilizador.remover_cliente(cliente["id"])
                print(Fore.GREEN + "Conta eliminada.")
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