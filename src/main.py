# ─────────────────────────────────────────────────────────────────────────────
# gui.py — Interface gráfica do Stand JDM usando Tkinter
# Corre este ficheiro diretamente: python gui.py
# ─────────────────────────────────────────────────────────────────────────────

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys, os

# Garante que os outros módulos do projeto são encontrados
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa os módulos do projeto
import cliente, carros, fornecedor, funcionario, stand, utils


# ─── CORES ───────────────────────────────────────────────────────────────────
# Paleta escura usada em toda a interface

BG    = "#1a1a2e"   # fundo principal (azul muito escuro)
PANEL = "#16213e"   # fundo de painéis e barras
ACCENT= "#e94560"   # cor de destaque (vermelho/rosa)
TEXT  = "#eaeaea"   # texto claro
GREEN = "#4caf50"   # botões de confirmação / sucesso
RED   = "#f44336"   # botões de perigo / eliminar
BTN   = "#0f3460"   # cor base dos botões normais


# ─── FONTES ───────────────────────────────────────────────────────────────────

F  = ("Segoe UI", 10)         # fonte normal
FB = ("Segoe UI", 10, "bold") # fonte a negrito


# ─── JANELA PRINCIPAL ─────────────────────────────────────────────────────────
# Criada uma única vez; o conteúdo é trocado com clear() + reconstrução

root = tk.Tk()
root.title("Stand JDM")
root.geometry("900x580")
root.configure(bg=BG)


# ─── UTILIZADOR ATUAL ─────────────────────────────────────────────────────────
# Usamos uma lista com um elemento porque Python não permite reatribuir
# variáveis simples dentro de funções aninhadas (seria preciso 'nonlocal')

user = [None]


# ─────────────────────────────────────────────────────────────────────────────
# FUNÇÕES AUXILIARES
# Pequenos helpers reutilizados em todo o ficheiro para evitar repetição
# ─────────────────────────────────────────────────────────────────────────────

def btn(parent, text, cmd, bg=BTN, **kw):
    """Cria e devolve um botão estilizado com efeito hover."""

    b = tk.Button(
        parent,
        text=text,
        command=cmd,
        bg=bg, fg=TEXT,
        font=FB,
        relief="flat",
        activebackground=ACCENT,
        activeforeground=TEXT,
        cursor="hand2",
        padx=10, pady=5,
        **kw
    )

    # Muda a cor quando o rato passa por cima (hover)
    b.bind("<Enter>", lambda e: b.config(bg=ACCENT))
    b.bind("<Leave>", lambda e: b.config(bg=bg))

    return b


def entry(parent, **kw):
    """Cria e devolve um campo de texto estilizado."""

    return tk.Entry(
        parent,
        font=F,
        bg=PANEL, fg=TEXT,
        insertbackground=TEXT,  # cor do cursor de texto
        relief="flat",
        **kw
    )


def label(parent, text, fg=TEXT, **kw):
    """Cria e devolve um label estilizado."""

    return tk.Label(parent, text=text, bg=BG, fg=fg, font=F, **kw)


def clear():
    """Apaga todos os widgets da janela principal para mostrar um novo ecrã."""

    for w in root.winfo_children():
        w.destroy()


def form_popup(title, campos, on_save, size="360x260"):
    """
    Abre uma janela popup com um formulário genérico.

    Parâmetros:
        title   — título da janela
        campos  — lista de tuplos (nome_campo, valor_inicial)
        on_save — função chamada ao guardar, recebe (dicionário_valores, janela)
        size    — dimensões da janela (largura x altura)
    """

    win = tk.Toplevel()
    win.title(title)
    win.configure(bg=BG)
    win.geometry(size)

    entries = {}

    # Cria um par label + entry para cada campo
    for i, (c, val) in enumerate(campos):
        label(win, c + ":").grid(row=i, column=0, sticky="w", padx=12, pady=3)
        e = entry(win, width=24)
        e.insert(0, val)  # pré-preenche com o valor inicial
        e.grid(row=i, column=1, padx=8, pady=3)
        entries[c] = e

    def save():
        # Recolhe todos os valores e valida que nenhum está vazio
        vals = {c: e.get().strip() for c, e in entries.items()}
        if not all(vals.values()):
            messagebox.showwarning("Atenção", "Preenche tudo.", parent=win)
            return
        on_save(vals, win)

    btn(win, "Guardar", save, GREEN).grid(
        row=len(campos), column=1, pady=10, sticky="e", padx=8
    )


def make_tree(parent, cols):
    """
    Cria e devolve um Treeview (tabela) estilizado com scrollbar.

    Parâmetros:
        parent — widget pai
        cols   — tuplo com os nomes das colunas
    """

    # Aplica estilos globais aos widgets ttk
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("Treeview",
                background=PANEL, foreground=TEXT,
                fieldbackground=PANEL, font=F, rowheight=24)
    s.configure("Treeview.Heading",
                background=BTN, foreground=TEXT, font=FB)
    s.configure("TNotebook",
                background=BG, borderwidth=0)
    s.configure("TNotebook.Tab",
                background=BTN, foreground=TEXT, font=FB, padding=[10, 5])
    s.map("TNotebook.Tab",
          background=[("selected", ACCENT)])  # tab ativa fica com a cor de destaque

    # Frame contentor da tabela + scrollbar
    f = tk.Frame(parent, bg=PANEL)
    f.pack(fill="both", expand=True, padx=8, pady=8)

    # Tabela
    t = ttk.Treeview(f, columns=cols, show="headings", height=12)
    for c in cols:
        t.heading(c, text=c)
        t.column(c, width=100, anchor="center")
    t.pack(side="left", fill="both", expand=True)

    # Scrollbar vertical ligada à tabela
    ttk.Scrollbar(f, orient="vertical", command=t.yview).pack(side="right", fill="y")

    return t


def drop_ids(fn):
    """
    Chama uma função de listagem e devolve só os IDs (chaves do dicionário).
    Usado para preencher os dropdowns de Stand e Fornecedor.
    """

    code, data = fn()
    return list(data.keys()) if code == 200 and isinstance(data, dict) else []


# ─────────────────────────────────────────────────────────────────────────────
# ECRÃ INICIAL
# ─────────────────────────────────────────────────────────────────────────────

def mostrar_inicio():
    """Mostra o ecrã inicial com as opções principais."""

    clear()

    # Frame centrado no meio da janela
    f = tk.Frame(root, bg=BG)
    f.place(relx=.5, rely=.5, anchor="center")

    tk.Label(f, text="🚗 STAND JDM",
             font=("Segoe UI", 24, "bold"), bg=BG, fg=ACCENT).pack(pady=(0, 20))

    btn(f, "Área Cliente", mostrar_login_cliente, width=20).pack(pady=5)
    btn(f, "Área Admin",   mostrar_login_admin,   width=20).pack(pady=5)
    btn(f, "Sair",         root.destroy, RED,     width=20).pack(pady=5)


# ─────────────────────────────────────────────────────────────────────────────
# LOGIN / REGISTO DE CLIENTE
# ─────────────────────────────────────────────────────────────────────────────

def mostrar_login_cliente():
    """Mostra o ecrã de login e registo de cliente."""

    clear()

    f = tk.Frame(root, bg=BG)
    f.place(relx=.5, rely=.5, anchor="center")

    tk.Label(f, text="LOGIN / REGISTO",
             font=("Segoe UI", 14, "bold"), bg=BG, fg=ACCENT).pack(pady=(0, 16))

    # ── Secção de login com ID ────────────────────────────────────────────────
    lf = tk.LabelFrame(f, text=" Entrar ", bg=PANEL, fg=TEXT, font=FB, padx=12, pady=10)
    lf.pack(fill="x", pady=4)

    label(lf, "ID:").grid(row=0, column=0, sticky="w")
    eid = entry(lf, width=18)
    eid.grid(row=0, column=1, padx=6)

    def login():
        # Tenta fazer login com o ID introduzido
        code, u = utils.fazer_login(eid.get().strip().upper())
        if code == 200:
            user[0] = u          # guarda o utilizador na variável global
            mostrar_menu_cliente()
        else:
            messagebox.showerror("Erro", "ID inválido.")

    btn(lf, "Entrar", login, GREEN).grid(row=0, column=2, padx=6)

    # ── Secção de registo de nova conta ──────────────────────────────────────
    rf = tk.LabelFrame(f, text=" Novo Registo ", bg=PANEL, fg=TEXT, font=FB, padx=12, pady=10)
    rf.pack(fill="x", pady=8)

    cs = ["Nome", "Data Nasc. (AAAA-MM-DD)", "Telefone",
          "Email", "Preferências", "Tipo (particular/empresa)"]
    es = {}

    for i, c in enumerate(cs):
        label(rf, c + ":").grid(row=i, column=0, sticky="w", pady=2)
        e = entry(rf, width=26)
        e.grid(row=i, column=1, padx=6, pady=2)
        es[c] = e

    def registar():
        vs = [es[c].get().strip() for c in cs]
        if not all(vs):
            messagebox.showwarning("Atenção", "Preenche tudo.")
            return
        code, msg = cliente.criar_cliente(*vs)
        if code == 201:
            messagebox.showinfo("OK", f"ID criado: {msg['id']}")
        else:
            messagebox.showerror("Erro", str(msg))

    btn(rf, "Registar", registar).grid(row=len(cs), column=1, pady=8, sticky="e")

    btn(f, "← Voltar", mostrar_inicio, bg="#555").pack(pady=8)


# ─────────────────────────────────────────────────────────────────────────────
# MENU PRINCIPAL DO CLIENTE
# ─────────────────────────────────────────────────────────────────────────────

def mostrar_menu_cliente():
    """Mostra o menu do cliente com barra de topo e painel de ações."""

    clear()
    u = user[0]

    # ── Barra de topo com info do utilizador ──────────────────────────────────
    top = tk.Frame(root, bg=PANEL, pady=8)
    top.pack(fill="x")

    tk.Label(top, text=f"👤 {u['nome']}  |  {u['id']}",
             bg=PANEL, fg=TEXT, font=FB).pack(side="left", padx=14)
    tk.Label(top, text=f"Saldo: {int(u['saldo'])}€",
             bg=PANEL, fg=GREEN, font=FB).pack(side="left")
    btn(top, "Logout", mostrar_inicio, RED).pack(side="right", padx=14)

    # ── Corpo: coluna de botões + painel de output ────────────────────────────
    body = tk.Frame(root, bg=BG)
    body.pack(fill="both", expand=True, padx=12, pady=8)

    # Coluna esquerda com os botões de ação
    col = tk.Frame(body, bg=BG)
    col.pack(side="left", fill="y", padx=(0, 12))

    # Área de texto à direita que mostra resultados (stock, perfil, etc.)
    out = tk.Text(body, bg=PANEL, fg=TEXT, font=("Consolas", 10),
                  relief="flat", wrap="word", state="disabled")
    out.pack(side="left", fill="both", expand=True, padx=4)

    def escrever(txt):
        """Substitui o conteúdo do painel de output pelo texto recebido."""
        out.config(state="normal")
        out.delete("1.0", "end")
        out.insert("end", txt)
        out.config(state="disabled")

    # ── Ações do cliente ──────────────────────────────────────────────────────

    def ver_stock():
        """Mostra todos os carros disponíveis no painel de output."""
        code, s = carros.listar_stock()
        if code == 200:
            texto = "STOCK\n\n" + "".join(
                f"  {m}  {c['marca']} {c['modelo']} ({c['ano']}) | {c['cor']} | {int(c['preco'])}€\n"
                for m, c in s.items()
            )
        else:
            texto = "Sem stock disponível."
        escrever(texto)

    def comprar():
        """Pede a matrícula ao utilizador e tenta comprar o carro."""
        mat = simpledialog.askstring("Comprar", "Matrícula:", parent=root)
        if not mat:
            return
        code, msg = utils.comprar_carro(u, mat.upper())
        (messagebox.showinfo if code == 200 else messagebox.showerror)("", msg)

    def saldo():
        """Permite ao utilizador depositar saldo na conta."""
        v = simpledialog.askstring("Saldo", "Valor (€):", parent=root)
        if not v:
            return
        code, msg = utils.carregar_saldo(u, v)
        if code == 200:
            messagebox.showinfo("OK", f"Novo saldo: {msg}€")
            mostrar_menu_cliente()  # atualiza a barra de topo com o novo saldo
        else:
            messagebox.showerror("Erro", str(msg))

    def perfil():
        """Mostra os dados do perfil no painel de output."""
        escrever(
            f"PERFIL\n\n"
            f"  ID:       {u['id']}\n"
            f"  Nome:     {u['nome']}\n"
            f"  Nasc:     {u['data_nascimento']}\n"
            f"  Tel:      {u['telefone']}\n"
            f"  Email:    {u['email']}\n"
            f"  Prefs:    {u['preferencias']}\n"
            f"  Tipo:     {u['tipo_compra']}\n"
            f"  Saldo:    {int(u['saldo'])}€\n"
            f"  Garagem:  {', '.join(u['carros']) or 'Vazia'}"
        )

    def editar():
        """Abre popup para editar os dados do perfil."""
        def save(vals, win):
            cliente.atualizar_cliente(
                u["id"], vals["Nome"], vals["Telefone"],
                vals["Email"], vals["Preferências"], vals["Tipo compra"]
            )
            messagebox.showinfo("OK", "Atualizado!", parent=win)
            win.destroy()

        form_popup("Editar Perfil", [
            ("Nome",         u["nome"]),
            ("Telefone",     u["telefone"]),
            ("Email",        u["email"]),
            ("Preferências", u["preferencias"]),
            ("Tipo compra",  u["tipo_compra"]),
        ], save)

    def apagar():
        """Remove a conta do cliente após confirmação."""
        if messagebox.askyesno("Confirmar", "Apagar conta?"):
            cliente.remover_cliente(u["id"])
            user[0] = None
            mostrar_inicio()

    # Cria os botões da coluna esquerda
    for txt, cmd in [
        ("🚗 Stock",    ver_stock),
        ("🛒 Comprar",  comprar),
        ("💰 Saldo",    saldo),
        ("👤 Perfil",   perfil),
        ("✏️ Editar",   editar),
        ("🗑 Apagar",   apagar),
    ]:
        btn(col, txt, cmd, width=16).pack(pady=4)


# ─────────────────────────────────────────────────────────────────────────────
# LOGIN ADMIN
# ─────────────────────────────────────────────────────────────────────────────

def mostrar_login_admin():
    """Pede a password de admin e abre o painel se estiver correta."""

    pw = simpledialog.askstring("Admin", "Password:", show="*")
    if pw == "chongolola":
        mostrar_menu_admin()
    else:
        messagebox.showerror("Erro", "Password incorreta.")


# ─────────────────────────────────────────────────────────────────────────────
# MENU ADMIN (com tabs: Carros / Fornecedores / Funcionários / Stands)
# ─────────────────────────────────────────────────────────────────────────────

def mostrar_menu_admin():
    """Mostra o painel de administração com 4 tabs."""

    clear()

    # ── Barra de topo ─────────────────────────────────────────────────────────
    top = tk.Frame(root, bg=PANEL, pady=8)
    top.pack(fill="x")

    tk.Label(top, text="⚙️ ADMIN",
             bg=PANEL, fg=ACCENT, font=("Segoe UI", 13, "bold")).pack(side="left", padx=14)
    btn(top, "← Início", mostrar_inicio, bg="#555").pack(side="right", padx=14)

    # ── Notebook (sistema de tabs) ────────────────────────────────────────────
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=10, pady=8)


    # ═════════════════════════════════════════════════════════════════════════
    # TAB: CARROS
    # ═════════════════════════════════════════════════════════════════════════

    tab_c = tk.Frame(nb, bg=BG)
    nb.add(tab_c, text="🚗 Carros")

    cols_c = ("Matrícula", "Marca", "Modelo", "Ano", "Cor", "Preço", "Stand", "Fornecedor")
    tree_c = make_tree(tab_c, cols_c)

    def refresh_c():
        """Recarrega a tabela de carros com o stock atual."""
        tree_c.delete(*tree_c.get_children())
        code, s = carros.listar_stock()
        if code == 200:
            for m, c in s.items():
                tree_c.insert("", "end", values=(
                    m, c["marca"], c["modelo"], c["ano"],
                    c["cor"], f"{int(c['preco'])}€", c["id_stand"], c["id_fornecedor"]
                ))

    def add_carro():
        """Abre popup para adicionar um novo carro ao stock."""
        win = tk.Toplevel()
        win.title("Novo Carro")
        win.configure(bg=BG)
        win.geometry("400x480")

        cs = ["Matrícula", "Marca", "Modelo", "Ano", "Preço", "Kms",
              "Cor", "Tração", "Portas", "Cilindrada", "Potência", "Lotação"]
        es = {}

        for i, c in enumerate(cs):
            label(win, c + ":").grid(row=i, column=0, sticky="w", padx=12, pady=2)
            e = entry(win, width=22)
            e.grid(row=i, column=1, padx=8, pady=2)
            es[c] = e

        # Dropdowns para escolher Stand e Fornecedor existentes
        sids = drop_ids(stand.listar_stands)
        fids = drop_ids(fornecedor.listar_fornecedores)
        vs = tk.StringVar(value=sids[0] if sids else "")
        vf = tk.StringVar(value=fids[0] if fids else "")

        for i, (lbl, var, ids) in enumerate([("Stand", vs, sids), ("Fornecedor", vf, fids)]):
            label(win, lbl + ":").grid(row=len(cs) + i, column=0, sticky="w", padx=12, pady=2)
            ttk.Combobox(win, textvariable=var, values=ids, width=20, state="readonly").grid(
                row=len(cs) + i, column=1, padx=8, pady=2
            )

        def save():
            vals = [es[c].get().strip() for c in cs]
            if not all(vals):
                messagebox.showwarning("Atenção", "Preenche tudo.", parent=win)
                return
            code, msg = carros.criar_carro(*vals, vs.get(), vf.get())
            if code == 201:
                # Associa o carro ao fornecedor se a função existir
                if hasattr(utils, "associar_carro_fornecedor"):
                    utils.associar_carro_fornecedor(vf.get(), vals[0].upper())
                messagebox.showinfo("OK", "Carro adicionado!", parent=win)
                win.destroy()
                refresh_c()
            else:
                messagebox.showerror("Erro", str(msg), parent=win)

        btn(win, "Guardar", save, GREEN).grid(
            row=len(cs) + 2, column=1, pady=10, sticky="e", padx=8
        )

    def rem_carro():
        """Remove o carro selecionado na tabela."""
        sel = tree_c.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Seleciona um carro.")
            return
        mat = tree_c.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirmar", f"Remover {mat}?"):
            code, msg = carros.remover_carro(mat)
            if code == 200:
                refresh_c()
            else:
                messagebox.showerror("Erro", str(msg))

    # Botões da tab de carros
    bf_c = tk.Frame(tab_c, bg=BG)
    bf_c.pack(fill="x", padx=8, pady=4)
    btn(bf_c, "➕ Adicionar", add_carro, GREEN).pack(side="left", padx=4)
    btn(bf_c, "🗑 Remover",   rem_carro, RED  ).pack(side="left", padx=4)
    btn(bf_c, "🔄 Atualizar", refresh_c       ).pack(side="left", padx=4)

    refresh_c()  # carrega a tabela ao abrir


    # ═════════════════════════════════════════════════════════════════════════
    # TAB: FORNECEDORES
    # ═════════════════════════════════════════════════════════════════════════

    tab_f = tk.Frame(nb, bg=BG)
    nb.add(tab_f, text="📦 Fornecedores")

    tree_f = make_tree(tab_f, ("ID", "Nome", "País", "Contacto", "Tipo", "Aval."))

    def refresh_f():
        """Recarrega a tabela de fornecedores."""
        tree_f.delete(*tree_f.get_children())
        code, data = fornecedor.listar_fornecedores()
        if code == 200:
            for fid, f in data.items():
                tree_f.insert("", "end", values=(
                    fid, f["nome"], f["pais"], f["contacto"], f["tipo"], f["avaliacao"]
                ))

    def add_f():
        """Abre popup para adicionar um novo fornecedor."""
        def save(vals, win):
            code, msg = fornecedor.criar_fornecedor(*vals.values())
            if code == 201:
                messagebox.showinfo("OK", f"ID: {msg['id']}", parent=win)
                win.destroy()
                refresh_f()
            else:
                messagebox.showerror("Erro", str(msg), parent=win)

        form_popup("Novo Fornecedor", [
            ("Nome", ""), ("Contacto", ""), ("País", ""),
            ("Email", ""), ("Tipo", ""), ("Morada", ""), ("Avaliação (1-5)", "")
        ], save, "360x310")

    def rem_f():
        """Remove o fornecedor selecionado na tabela."""
        sel = tree_f.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Seleciona.")
            return
        fid = str(tree_f.item(sel[0])["values"][0])
        if messagebox.askyesno("Confirmar", f"Remover {fid}?"):
            code, msg = fornecedor.remover_fornecedor(fid)
            if code == 200:
                refresh_f()
            else:
                messagebox.showerror("Erro", str(msg))

    bf_f = tk.Frame(tab_f, bg=BG)
    bf_f.pack(fill="x", padx=8, pady=4)
    btn(bf_f, "➕ Adicionar", add_f,    GREEN).pack(side="left", padx=4)
    btn(bf_f, "🗑 Remover",   rem_f,    RED  ).pack(side="left", padx=4)
    btn(bf_f, "🔄 Atualizar", refresh_f      ).pack(side="left", padx=4)

    refresh_f()


    # ═════════════════════════════════════════════════════════════════════════
    # TAB: FUNCIONÁRIOS
    # ═════════════════════════════════════════════════════════════════════════

    tab_fn = tk.Frame(nb, bg=BG)
    nb.add(tab_fn, text="👔 Funcionários")

    tree_fn = make_tree(tab_fn, ("ID", "Nome", "Cargo", "Salário", "Turno", "Stand"))

    def refresh_fn():
        """Recarrega a tabela de funcionários."""
        tree_fn.delete(*tree_fn.get_children())
        code, data = funcionario.listar_funcionarios()
        if code == 200:
            for fid, f in data.items():
                tree_fn.insert("", "end", values=(
                    fid, f["nome"], f["cargo"], f"{f['salario']}€", f["turno"], f["id_stand"]
                ))

    def add_fn():
        """Abre popup para adicionar um novo funcionário."""
        win = tk.Toplevel()
        win.title("Novo Funcionário")
        win.configure(bg=BG)
        win.geometry("380x340")

        cs = ["Nome", "Cargo", "Salário", "Telefone", "Turno", "NIF", "IBAN"]
        es = {}

        for i, c in enumerate(cs):
            label(win, c + ":").grid(row=i, column=0, sticky="w", padx=12, pady=3)
            e = entry(win, width=24)
            e.grid(row=i, column=1, padx=8, pady=3)
            es[c] = e

        # Dropdown para escolher o stand onde o funcionário trabalha
        sids = drop_ids(stand.listar_stands)
        vs2 = tk.StringVar(value=sids[0] if sids else "")
        label(win, "Stand:").grid(row=len(cs), column=0, sticky="w", padx=12, pady=3)
        ttk.Combobox(win, textvariable=vs2, values=sids, width=20, state="readonly").grid(
            row=len(cs), column=1, padx=8, pady=3
        )

        def save():
            vals = [es[c].get().strip() for c in cs]
            if not all(vals):
                messagebox.showwarning("Atenção", "Preenche tudo.", parent=win)
                return
            code, msg = funcionario.criar_funcionario(*vals, vs2.get())
            if code == 201:
                messagebox.showinfo("OK", f"ID: {msg['id']}", parent=win)
                win.destroy()
                refresh_fn()
            else:
                messagebox.showerror("Erro", str(msg), parent=win)

        btn(win, "Guardar", save, GREEN).grid(
            row=len(cs) + 1, column=1, pady=10, sticky="e", padx=8
        )

    def rem_fn():
        """Remove o funcionário selecionado na tabela."""
        sel = tree_fn.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Seleciona.")
            return
        fid = str(tree_fn.item(sel[0])["values"][0])
        if messagebox.askyesno("Confirmar", f"Remover {fid}?"):
            code, msg = funcionario.remover_funcionario(fid)
            if code == 200:
                refresh_fn()
            else:
                messagebox.showerror("Erro", str(msg))

    bf_fn = tk.Frame(tab_fn, bg=BG)
    bf_fn.pack(fill="x", padx=8, pady=4)
    btn(bf_fn, "➕ Adicionar", add_fn,    GREEN).pack(side="left", padx=4)
    btn(bf_fn, "🗑 Remover",   rem_fn,    RED  ).pack(side="left", padx=4)
    btn(bf_fn, "🔄 Atualizar", refresh_fn       ).pack(side="left", padx=4)

    refresh_fn()


    # ═════════════════════════════════════════════════════════════════════════
    # TAB: STANDS
    # ═════════════════════════════════════════════════════════════════════════

    tab_s = tk.Frame(nb, bg=BG)
    nb.add(tab_s, text="🏢 Stands")

    tree_s = make_tree(tab_s, ("ID", "Nome", "Morada", "Telefone", "Email", "NIF"))

    def refresh_s():
        """Recarrega a tabela de stands."""
        tree_s.delete(*tree_s.get_children())
        code, data = stand.listar_stands()
        if code == 200:
            for sid, s in data.items():
                tree_s.insert("", "end", values=(
                    sid, s["nome"], s["morada"], s["telefone"], s["email"], s["nif"]
                ))

    def add_s():
        """Abre popup para adicionar um novo stand."""
        def save(vals, win):
            code, msg = stand.criar_stand(*vals.values())
            if code == 201:
                messagebox.showinfo("OK", f"ID: {msg['id']}", parent=win)
                win.destroy()
                refresh_s()
            else:
                messagebox.showerror("Erro", str(msg), parent=win)

        form_popup("Novo Stand", [
            ("Nome", ""), ("Morada", ""), ("Telefone", ""), ("Email", ""), ("NIF", "")
        ], save)

    bf_s = tk.Frame(tab_s, bg=BG)
    bf_s.pack(fill="x", padx=8, pady=4)
    btn(bf_s, "➕ Adicionar", add_s,    GREEN).pack(side="left", padx=4)
    btn(bf_s, "🔄 Atualizar", refresh_s      ).pack(side="left", padx=4)

    refresh_s()


# ─────────────────────────────────────────────────────────────────────────────
# ARRANQUE DA APLICAÇÃO
# ─────────────────────────────────────────────────────────────────────────────

# Se comprar_carro não estiver implementado em utils.py, usa um placeholder
if not hasattr(utils, "comprar_carro"):
    utils.comprar_carro = lambda u, m: (501, "comprar_carro não implementado em utils.py")

# Se associar_carro_fornecedor não existir, usa uma função que não faz nada
if not hasattr(utils, "associar_carro_fornecedor"):
    utils.associar_carro_fornecedor = lambda f, m: None

# Mostra o ecrã inicial e arranca o loop de eventos do Tkinter
mostrar_inicio()
root.mainloop()