import cliente
import carros
import fornecedor
import funcionario
import stand
import time, sys
from colorama import Fore, Back, Style, init

init(autoreset=True)

def loading_bar(texto):
    print(Fore.WHITE + texto, end="")
    for _ in range(15):
        time.sleep(0.03)
        sys.stdout.write(Fore.GREEN + "█")
        sys.stdout.flush()
    print(" OK!")

# ─── LOGIN ────────────────────────────────────────────────────────────────────
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
        nome      = input("Nome: ")
        data_nasc = input("Data de nascimento (YYYY-MM-DD): ")
        tel       = input("Telefone: ")
        mail      = input("Email: ")
        prefs     = input("Preferências (ex: JDM, SUV): ")
        tipo      = input("Tipo de compra (particular/empresa): ")
        code, msg = cliente.criar_cliente(nome, data_nasc, tel, mail, prefs, tipo)
        if code == 201:
            print(Fore.GREEN + f"Conta criada! O teu ID é: {msg['id']}")
        else:
            print(Fore.RED + str(msg))

    elif op == "0":
        exit()

    return None

# ─── MENU CLIENTE ─────────────────────────────────────────────────────────────
def menu_cliente(u):
    while True:
        print("\n" + Back.WHITE + Fore.BLACK + f"  ID: {u['id']} | {u['nome']}  " + Style.RESET_ALL + Fore.GREEN + f"  Saldo: {int(u['saldo'])}€")
        print("1. Stock | 2. Comprar | 3. Saldo | 4. Perfil | 5. Editar | 6. Apagar | 0. Logout")
        op = input("\nComando: ").strip()

        if op == "1":
            code, stock = carros.listar_stock()
            if code == 200:
                print(f"\n{Fore.CYAN}{'=' * 55}")
                print(f"{Fore.WHITE}{Style.BRIGHT}           INVENTÁRIO STAND JDM")
                print(f"{Fore.CYAN}{'=' * 55}")
                for d, _ in stock:
                    print(f"{Fore.YELLOW}{d[0]}{Fore.WHITE} | {d[1]} {d[2]} {d[3]} | {d[6]} | {Fore.GREEN}{int(d[4])}€")
            else:
                print(Fore.RED + "Sem stock disponível.")
            input("\nEnter para continuar...")

        elif op == "2":
            mat = input("\nDigite a matrícula: ").strip().upper()
            code, msg = carros.comprar_carro(u, mat)
            print(Fore.GREEN + msg if code == 200 else Fore.RED + msg)

        elif op == "3":
            valor = input("\nValor a depositar (€): ")
            code, msg = cliente.carregar_saldo(u, valor)
            print(Fore.GREEN + f"Novo saldo: {msg}€" if code == 200 else Fore.RED + str(msg))

        elif op == "4":
            code, obj = cliente.ver_perfil(u)
            print(f"\n{Fore.YELLOW}--- O TEU PERFIL ---")
            print(f"ID: {obj['id']} | Nome: {obj['nome']} | Nasc: {obj['data_nascimento']}")
            print(f"Tel: {obj['telefone']} | Email: {obj['email']}")
            print(f"Preferências: {obj['preferencias']} | Tipo: {obj['tipo_compra']}")
            print(f"Membro desde: {obj['data_registo']}")
            print(f"Garagem: {Fore.CYAN}{', '.join(obj['carros']) if obj['carros'] else 'Vazia'}")
            input("\nEnter para voltar...")

        elif op == "5":
            print(f"\n{Fore.YELLOW}--- EDITAR PERFIL (Vazio para manter) ---")
            n  = input(f"Nome [{u['nome']}]: ").strip()
            t  = input(f"Tel [{u['telefone']}]: ").strip()
            e  = input(f"Email [{u['email']}]: ").strip()
            p  = input(f"Preferências [{u['preferencias']}]: ").strip()
            tc = input(f"Tipo compra [{u['tipo_compra']}]: ").strip()
            code, msg = cliente.atualizar_cliente(u["id"], n or None, t or None, e or None, p or None, tc or None)
            print(Fore.BLUE + msg if code == 200 else Fore.RED + msg)

        elif op == "6":
            confirma = input(Fore.RED + "Tens a certeza? (s/n): ").lower()
            if confirma == 's':
                code, msg = cliente.remover_cliente(u["id"])
                print(Fore.RED + msg)
                if code == 200:
                    break

        elif op == "0":
            break

# ─── MENU ADMIN ───────────────────────────────────────────────────────────────
def menu_admin():
    while True:
        print(f"\n{Fore.MAGENTA}===== MENU ADMIN =====")
        print("1. Listar Carros  | 2. Adicionar Carro  | 3. Remover Carro")
        print("4. Listar Fornec. | 5. Adicionar Fornec.| 6. Remover Fornec.")
        print("7. Listar Func.   | 8. Adicionar Func.  | 9. Remover Func.")
        print("A. Listar Stands  | B. Adicionar Stand  |")
        print("0. Sair")
        op = input("\nComando: ").strip().upper()

        if op == "1":
            code, stock = carros.listar_stock()
            if code == 200:
                for d, _ in stock:
                    print(f"{Fore.YELLOW}{d[0]} | {d[1]} {d[2]} {d[3]} | {d[6]} | {int(d[4])}€ | Stand:{d[12]} | Forn:{d[13]}")
            else:
                print(Fore.RED + "Sem stock.")
            input("\nEnter para continuar...")

        elif op == "2":
            mat  = input("Matrícula: ").upper().strip()
            marc = input("Marca: ");      mod  = input("Modelo: ")
            ano  = input("Ano: ");        pre  = input("Preço: ")
            kms  = input("Kms: ");        cor  = input("Cor: ")
            tra  = input("Tração: ");     por  = input("Nº Portas: ")
            cil  = input("Cilindrada: "); pot  = input("Potência(cv): ")
            lot  = input("Lotação: ")
            # mostrar stands e fornecedores disponíveis
            _, stands_list = stand.listar_stands()
            print(f"\n{Fore.CYAN}Stands disponíveis:")
            for sid, s in stands_list.items():
                print(f"  {sid} - {s['nome']}")
            ids = input("ID Stand: ").upper().strip()

            _, forn_list = fornecedor.listar_fornecedores()
            print(f"\n{Fore.CYAN}Fornecedores disponíveis:")
            for fid, f in forn_list.items():
                print(f"  {fid} - {f['nome']} ({f['pais']})")
            idf = input("ID Fornecedor: ").upper().strip()
            code, msg = carros.criar_carro(mat, marc, mod, ano, pre, kms, cor, tra, por, cil, pot, lot, ids, idf)
            print(Fore.GREEN + "Carro adicionado!" if code == 201 else Fore.RED + str(msg))

        elif op == "3":
            mat = input("Matrícula: ").upper().strip()
            code, msg = carros.remover_carro(mat)
            print(Fore.GREEN + msg if code == 200 else Fore.RED + msg)

        elif op == "4":
            code, lista = fornecedor.listar_fornecedores()
            if code == 200:
                for fid, f in lista.items():
                    print(f"{Fore.YELLOW}{fid} | {f['nome']} | {f['pais']} | Aval:{f['avaliacao']}")
            else:
                print(Fore.RED + str(lista))
            input("\nEnter para continuar...")

        elif op == "5":
            nome = input("Nome: ");      cont = input("Contacto: ")
            pais = input("País: ");      mail = input("Email: ")
            tipo = input("Tipo: ");      mor  = input("Morada: ")
            aval = input("Avaliação(1-5): ")
            code, msg = fornecedor.criar_fornecedor(nome, cont, pais, mail, tipo, mor, aval)
            print(Fore.GREEN + f"Fornecedor criado! ID: {msg['id']}" if code == 201 else Fore.RED + str(msg))

        elif op == "6":
            code, lista = fornecedor.listar_fornecedores()
            for fid, f in lista.items():
                print(f"  {fid} - {f['nome']}")
            fid = input("ID Fornecedor: ").upper().strip()
            code, msg = fornecedor.remover_fornecedor(fid)
            print(Fore.GREEN + msg if code == 200 else Fore.RED + msg)

        elif op == "7":
            code, lista = funcionario.listar_funcionarios()
            if code == 200:
                for fid, f in lista.items():
                    print(f"{Fore.YELLOW}{fid} | {f['nome']} | {f['cargo']} | {f['salario']}€ | Stand:{f['id_stand']}")
            else:
                print(Fore.RED + str(lista))
            input("\nEnter para continuar...")

        elif op == "8":
            nome  = input("Nome: ");    cargo = input("Cargo: ")
            sal   = input("Salário: "); tel   = input("Telefone: ")
            turno = input("Turno (manhã/tarde/noite): ")
            nif   = input("NIF: ");     iban  = input("IBAN: ")
            _, stands_list = stand.listar_stands()
            print(f"\n{Fore.CYAN}Stands disponíveis:")
            for sid, s in stands_list.items():
                print(f"  {sid} - {s['nome']}")
            ids = input("ID Stand: ").upper().strip()
            code, msg = funcionario.criar_funcionario(nome, cargo, sal, tel, turno, nif, iban, ids)
            print(Fore.GREEN + f"Funcionário criado! ID: {msg['id']}" if code == 201 else Fore.RED + str(msg))

        elif op == "9":
            code, lista = funcionario.listar_funcionarios()
            for fid, f in lista.items():
                print(f"  {fid} - {f['nome']}")
            fid = input("ID Funcionário: ").upper().strip()
            code, msg = funcionario.remover_funcionario(fid)
            print(Fore.GREEN + msg if code == 200 else Fore.RED + msg)

        elif op == "A":
            code, lista = stand.listar_stands()
            if code == 200:
                for sid, s in lista.items():
                    print(f"{Fore.YELLOW}{sid} | {s['nome']} | {s['morada']} | Fornec:{s['lista_ids_fornecedores']}")
            else:
                print(Fore.RED + str(lista))
            input("\nEnter para continuar...")

        elif op == "B":
            nome = input("Nome: ");  mor  = input("Morada: ")
            tel  = input("Tel: ");   mail = input("Email: ");  nif = input("NIF: ")
            code, msg = stand.criar_stand(nome, mor, tel, mail, nif)
            print(Fore.GREEN + f"Stand criado! ID: {msg['id']}" if code == 201 else Fore.RED + str(msg))


        elif op == "0":
            break

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    while True:
        print(f"\n{Fore.MAGENTA}===================================")
        print(f"{Fore.WHITE}{Style.BRIGHT}           STAND JDM")
        print(f"{Fore.MAGENTA}===================================")
        print("1. Área Cliente | 2. Área Admin | 0. Sair")
        op = input("\nEscolha: ").strip()
        if op == "1":
            u = login()
            if u:
                menu_cliente(u)
        elif op == "2":
            passe = input("Password admin: ").strip()
            if passe != "chongolola":
                print(Fore.RED + "Password incorreta.")
                continue
            menu_admin()
        elif op == "0":
            break

if __name__ == "__main__":
    main()
