# 🚗 Stand JDM - Sistema de Gestão (CLI)

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-CLI-lightgrey)

---

## 📌 Descrição

Um projeto em Python que simula um stand de carros JDM (Japanese Domestic Market), com sistema de clientes, compra de veículos, gestão de saldo e administração de stands, fornecedores e funcionários — tudo através do terminal.

---

## 🚀 Funcionalidades

### Área Cliente
- 🔐 Sistema de login e registo de clientes (ID gerado automaticamente)
- 💰 Gestão de saldo (depósitos)
- 🚘 Visualização de stock disponível
- 🛒 Compra de veículos
- 👤 Ver e editar perfil
- ❌ Apagar conta

### Área Admin *(password protegida)*
- 🚗 Gestão de carros (listar, adicionar, remover)
- 🏢 Gestão de stands (listar, adicionar)
- 🤝 Gestão de fornecedores (listar, adicionar, remover)
- 👷 Gestão de funcionários (listar, adicionar, remover)
- 🔗 Associar fornecedores a stands

---

## 🗂️ Estrutura do Projeto

```
stand_de_automoveis/
└── src/
    ├── main.py          # Menu principal e interface CLI
    ├── carros.py        # CRUD de veículos
    ├── cliente.py       # CRUD de clientes
    ├── fornecedor.py    # CRUD de fornecedores
    ├── fornecimento.py  # Relação stand ↔ fornecedor
    ├── funcionario.py   # CRUD de funcionários
    ├── stand.py         # CRUD de stands
    └── utils.py         # Funções auxiliares
```

---

## 🧩 Entidades

| Entidade | Descrição |
|---|---|
| **Carro** | Veículos disponíveis no stand com dados técnicos completos |
| **Cliente** | Utilizadores registados que podem comprar carros |
| **Fornecedor** | Empresas que fornecem veículos ao stand |
| **Funcionário** | Colaboradores do stand |
| **Stand** | Localizações físicas do Stand JDM |
| **Fornecimento** | Relação entre stands e fornecedores |

---

## ▶️ Como correr

```bash
cd src
python main.py
```

### Requisitos
```bash
pip install colorama
```

---

## 📄 Licença

MIT
