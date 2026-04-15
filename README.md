🚗 Stand JDM - Sistema de Gestão (CLI)

Um pequeno projeto em Python que simula um stand de carros JDM (Japanese Domestic Market), com sistema de clientes, compra de veículos e gestão de saldo — tudo através do terminal.

📌 Funcionalidades
🔐 Sistema de login e registo de clientes
💰 Gestão de saldo
🚘 Visualização de stock de carros
🛒 Compra de veículos
👤 Perfil do utilizador
✏️ Edição de dados do cliente
❌ Remoção de conta
🧠 Estrutura do Projeto

O projeto está dividido em 3 módulos principais:

main.py → Interface principal e navegação (menus, login, etc.)
carros.py → Gestão do stock e compras de carros
cliente.py → Gestão dos clientes (CRUD)
🛠️ Tecnologias Utilizadas
Python 3
Biblioteca colorama (para cores no terminal)
📦 Instalação
Clona o repositório:
git clone https://github.com/teu-username/stand-jdm.git
cd stand-jdm
Instala as dependências:
pip install colorama
Executa o programa:
python main.py
🎮 Como Usar
Inicia o programa
Cria uma conta ou faz login
Navega pelo menu:
Ver stock
Comprar carros
Adicionar saldo
Ver/editar perfil
🚗 Carros Disponíveis

O sistema inclui alguns clássicos JDM:

Nissan Skyline R34
Toyota Supra MK4
Mazda RX-7 FD
Honda NSX
Mitsubishi Lancer Evo IX
Subaru Impreza 22B
Nissan Silvia S15
Toyota AE86 Trueno
⚠️ Notas
Os dados são guardados apenas em memória (não persistem após fechar o programa)
Ideal para aprendizagem de Python e conceitos como:
Estruturas de dados
Modularização
CRUD
Interação com utilizador
💡 Melhorias Futuras
💾 Guardar dados em ficheiro (JSON ou base de dados)
🔑 Sistema de autenticação mais seguro
🖥️ Interface gráfica (Tkinter ou Web)
📊 Histórico de compras
