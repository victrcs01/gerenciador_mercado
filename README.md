# Gerenciador de Mercado

Este projeto é um sistema de gerenciamento de mercado desenvolvido em Python, utilizando uma interface de linha de comando (CLI). Ele simula as operações de um Mercado, permitindo a interação de dois tipos de usuários: **Clientes** e **Administradores**. O sistema gerencia produtos (físicos e digitais), estoque, pedidos e usuários, com persistência de dados em arquivos Excel.

O projeto foi desenvolvido para a disciplina de **ANÁLISE, PROJETO E PROGRAMAÇÃO ORIENTADOS A OBJETOS** do curso de Engenharia de Sistemas da UFMG.

## ✨ Funcionalidades

- **Autenticação de Usuários:** Sistema de login para diferenciar clientes e administradores.
- **Menus Interativos:** Interfaces de linha de comando distintas e intuitivas para cada tipo de usuário, construídas com a biblioteca `rich`.
- **Gerenciamento de Produtos (CRUD):** Administradores podem cadastrar, visualizar, editar e remover produtos.
- **Controle de Estoque:** A quantidade de produtos físicos é atualizada automaticamente a cada venda ou remoção de item do carrinho.
- **Distinção entre Produtos Físicos e Digitais:** O sistema lida com as particularidades de cada tipo, como estoque para físicos e links de download para digitais.
- **Processo de Compra Completo:** Clientes podem visualizar produtos, montar um carrinho de compras (adicionando e removendo itens), concluir o pedido e verificar seu histórico.
- **Gerenciamento de Pedidos:** Administradores podem visualizar todos os pedidos do sistema e processar as entregas, atualizando o status de cada pedido.
- **Persistência de Dados:** Todas as informações de usuários, produtos e pedidos são salvas em arquivos `.xlsx`, utilizando a biblioteca `pandas`.
- **Código Orientado a Objetos:** O projeto é estruturado com base nos princípios de POO, como encapsulamento, herança e polimorfismo, para garantir um código limpo, modular e extensível.

## 🚀 Tecnologias Utilizadas

- **Python 3**
- **Rich:** Para a criação de interfaces de usuário ricas e coloridas no terminal.
- **Pandas:** Para a manipulação e persistência de dados em arquivos Excel.

## ⚙️ Como Executar

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/gerenciador_mercado.git
    cd gerenciador_mercado
    ```

2.  **Instale as dependências:**
    ```bash
    pip install rich pandas openpyxl
    ```
    *(O `openpyxl` é necessário para o pandas manipular arquivos .xlsx)*

3.  **Execute o programa:**
    ```bash
    python src/main.py
    ```
    *(Assumindo que o ponto de entrada do seu projeto é `src/main.py`)*

## 🏛️ Estrutura do Projeto

O projeto segue uma arquitetura orientada a objetos para garantir a separação de responsabilidades e a manutenibilidade.

- `Usuario`: Classe base para todos os usuários do sistema.
- `Admin`: Herda de `Usuario` e contém as funcionalidades administrativas.
- `Produto`: Classe base abstrata para os produtos.
- `ProdutoFisico` e `ProdutoDigital`: Herdam de `Produto` e implementam suas lógicas específicas.
- `Pedido`: Representa um carrinho de compras/pedido de um cliente.
- `Mercado`: Classe principal que age como um controlador, orquestrando as interações entre usuários, produtos e pedidos.
- `BancoDeDados`: Classe responsável por ler e escrever os DataFrames do `pandas` nos arquivos Excel.
- `ExibirProdutos`: Classe base que fornece um método polimórfico para exibir tabelas de produtos, usada por `Mercado` e `Pedido`.