import pandas as pd
import json
from banco_de_dados import BancoDeDados
from exibir_produtos import ExibirProdutos
from pedido import Pedido
from produto import Produto
from produto_digital import ProdutoDigital
from produto_fisico import ProdutoFisico
from rich.console import Console
from rich.prompt import Prompt, FloatPrompt, IntPrompt
from rich.table import Table

class Mercado(ExibirProdutos):

    def __init__(self):
        """
        Inicializa o mercado com uma lista de produtos e pedidos
        """
        super().__init__(self.carregar_produtos())
        self._pedidos = self.carregar_pedidos()

    def carregar_pedidos(self, cliente_id: int | None = None) -> list[Pedido]:
        """
        Carrega os pedidos do sistema a partir do banco de dados.
        Se um cliente_id for fornecido, carrega apenas os pedidos desse cliente.
        """
        tabela_pedidos = BancoDeDados().carregar_tabela("pedidos")

        if tabela_pedidos.empty:
            return []

        if cliente_id is not None:
            # Garante que a coluna 'cliente_id' e o valor são do mesmo tipo para comparação
            tabela_pedidos = tabela_pedidos[tabela_pedidos['cliente_id'].astype(int) == cliente_id]

        lista_pedidos = []

        for row in tabela_pedidos.itertuples(index=False):
            produtos_no_pedido = []
            # Desserializa a string JSON de produtos
            itens_serializados = json.loads(row.produtos)
            
            for item in itens_serializados:
                produto_original = self._produtos.get(item['id'])
                if produto_original:
                    if isinstance(produto_original, ProdutoFisico):
                        # Cria uma instância específica para o pedido com a quantidade comprada
                        produto_para_pedido = produto_original.realizar_venda(item['quantidade'])
                        produto_original.quantidade += item['quantidade'] # Devolve ao estoque para não duplicar a remoção
                    else: # ProdutoDigital
                        produto_para_pedido = produto_original.realizar_venda()
                    produtos_no_pedido.append(produto_para_pedido)

            pedido = Pedido(id=row.id, cliente_id=row.cliente_id, produtos=produtos_no_pedido,
                            data=pd.to_datetime(row.data), status=row.status)
            lista_pedidos.append(pedido)
        return lista_pedidos
    
    def carregar_produtos(self) -> dict[int, Produto]:
        """
        Carrega os produtos disponíveis no mercado a partir do banco de dados.
        Retorna um dicionário de produtos.
        """
        tabela_produtos = BancoDeDados().carregar_tabela("produtos")
        dicionario_produtos = {}

        if tabela_produtos.empty:
            return dicionario_produtos

        for row in tabela_produtos.itertuples(index=False):
            if row.tipo == 'digital':
                produto = ProdutoDigital(id=row.id, nome=row.nome, preco=row.preco, link_download=row.link_download)
            elif row.tipo == 'fisico':
                produto = ProdutoFisico(id=row.id, nome=row.nome, preco=row.preco, quantidade=row.quantidade, altura=row.altura, largura=row.largura, profundidade=row.profundidade)
            
            dicionario_produtos[int(row.id)] = produto

        return dicionario_produtos

    def salvar_produtos(self):
        """
        Converte a lista de produtos em um DataFrame e salva no banco de dados.
        """
        # Usa o método get_dic de cada produto para criar a lista de dicionários,
        # aproveitando o polimorfismo.
        lista_para_df = [produto.get_dic() for produto in self._produtos.values()]
        df_produtos = pd.DataFrame(lista_para_df)
        BancoDeDados().salvar_tabela(df_produtos, "produtos")

    def salvar_pedidos(self):
        """
        Converte a lista de pedidos em um DataFrame e salva no banco de dados.
        """
        if not self._pedidos:
            return
        lista_para_df = [pedido.get_dic() for pedido in self._pedidos]
        df_pedidos = pd.DataFrame(lista_para_df)
        BancoDeDados().salvar_tabela(df_pedidos, "pedidos")

    def cadastrar_produto(self):
        """
        Solicita os dados de um novo produto ao usuário, o instancia
        e o adiciona à lista de produtos do mercado.
        """
        console = Console()
        console.print("\n[bold yellow]----- Cadastro de Novo Produto -----[/bold yellow]")

        tipo_produto = Prompt.ask("O produto é [bold]Físico[/] ou [bold]Digital[/]?", choices=["fisico", "digital"], default="fisico").lower()

        nome = Prompt.ask("Nome do produto")
        preco = FloatPrompt.ask("Preço (R$)", default=0.0)

        novo_id = max(self._produtos.keys()) + 1 if self._produtos else 1

        if tipo_produto == 'fisico':
            quantidade = IntPrompt.ask("Quantidade em estoque", default=100)
            altura = FloatPrompt.ask("Altura (cm)", default=10.0)
            largura = FloatPrompt.ask("Largura (cm)", default=10.0)
            profundidade = FloatPrompt.ask("Profundidade (cm)", default=10.0)
            novo_produto = ProdutoFisico(id=novo_id, nome=nome, preco=preco, quantidade=quantidade, altura=altura, largura=largura, profundidade=profundidade)
        else:  # digital
            link_download = Prompt.ask("Link para download")
            novo_produto = ProdutoDigital(id=novo_id, nome=nome, preco=preco, link_download=link_download)

        self._produtos[novo_id] = novo_produto
        self.salvar_produtos()
        console.print(f"\n[bold green]Produto '{nome}' cadastrado com sucesso com o ID {novo_id}![/]")

    def editar_produto(self):
        """
        Permite ao administrador selecionar um produto e editar suas informações,
        delegando a lógica de edição para o próprio objeto do produto.
        """
        console = Console()
        console.print("\n[bold yellow]----- Edição de Produto -----[/bold yellow]")

        id_produto = self.selecionar_produto()
        if id_produto is None:
            return

        produto = self._produtos.get(id_produto)
        
        # Polimorfismo: Chama o método de edição específico da classe do produto
        produto.exibir_menu_edicao()

        self.salvar_produtos()
        console.print(f"\n[bold green]Produto '{produto.nome}' (ID: {produto.id}) salvo com sucesso![/]")

    def fazer_novo_pedido(self, cliente_id: int):
        """
        Inicia o processo de criação de um novo pedido para um cliente.

        Args:
            cliente_id: O ID do cliente que está fazendo o pedido.
        """
        console = Console()
        
        novo_id_pedido = len(self._pedidos) + 1
        novo_pedido = Pedido(id=novo_id_pedido, cliente_id=cliente_id)
        
        while True:
            console.print(f"\n[bold]Pedido nº {novo_pedido.id}[/] | [cyan]{len(novo_pedido.produtos)} itens[/] | [bold green]Total: R$ {novo_pedido.calcular_total():.2f}[/]")
            
            # O método exibir_produtos é herdado por Pedido e mostrará os itens do pedido
            novo_pedido.exibir_produtos()

            console.print("\n[bold magenta]----- Opções do Pedido -----[/bold magenta]")
            console.print("[cyan]1.[/] Adicionar Item")
            console.print("[cyan]2.[/] Remover Item")
            console.print("[cyan]3.[/] Concluir Pedido")

            escolha = Prompt.ask("[bold]O que deseja fazer?[/]", choices=["1", "2", "3"])

            if escolha == "1":
                console.print("\n[bold yellow]----- Adicionar Item ao Pedido -----[/bold yellow]")
                
                # 1. Seleciona o produto do catálogo do mercado
                id_produto_mercado = self.selecionar_produto()
                if id_produto_mercado is None:
                    continue  # Volta ao menu do pedido se nada for selecionado

                produto_no_mercado = self._produtos.get(id_produto_mercado)

                # 2. Define a quantidade e realiza a venda
                produto_para_pedido = None
                if isinstance(produto_no_mercado, ProdutoFisico):
                    while True:
                        quantidade_desejada = IntPrompt.ask(
                            f"Digite a quantidade para '{produto_no_mercado.nome}' (Estoque: {produto_no_mercado.quantidade})",
                            default=1
                        )
                        if 0 < quantidade_desejada <= produto_no_mercado.quantidade:
                            # Cria uma nova instância para o pedido e atualiza o estoque do mercado
                            produto_para_pedido = produto_no_mercado.realizar_venda(quantidade_desejada)
                            self.salvar_produtos()  # Salva o estoque atualizado
                            break
                        else:
                            console.print(f"[bold red]Quantidade inválida. Insira um valor entre 1 e {produto_no_mercado.quantidade}.[/]")
                elif isinstance(produto_no_mercado, ProdutoDigital):
                    produto_para_pedido = produto_no_mercado.realizar_venda()

                # 3. Adiciona a nova instância do produto ao pedido
                novo_pedido.adicionar_produto(produto_para_pedido)
            elif escolha == "2":
                if not novo_pedido.produtos:
                    console.print("\n[yellow]O carrinho está vazio. Não há itens para remover.[/yellow]")
                    continue

                console.print("\n[bold yellow]----- Remover Item do Pedido -----[/bold yellow]")
                
                # Cria um menu de remoção com os itens do pedido
                opcoes_remocao = {}
                for i, produto_no_pedido in enumerate(novo_pedido.produtos):
                    if isinstance(produto_no_pedido, ProdutoFisico):
                        label = f"{produto_no_pedido.nome} (Quantidade: {produto_no_pedido.quantidade})"
                    else:
                        label = f"{produto_no_pedido.nome} (Digital)"
                    
                    opcoes_remocao[str(i + 1)] = i # Armazena o índice
                    console.print(f"  [cyan]{i + 1}.[/] {label}")

                cancelar_opcao = str(len(opcoes_remocao) + 1)
                console.print(f"  [cyan]{cancelar_opcao}.[/] Cancelar")

                escolha_remocao = Prompt.ask("\n[bold]Qual item deseja remover?[/]", choices=[*opcoes_remocao.keys(), cancelar_opcao])

                if escolha_remocao == cancelar_opcao:
                    continue

                # Remove o item da lista do pedido
                indice_para_remover = int(escolha_remocao) - 1
                item_removido = novo_pedido.remover_produto_por_indice(indice_para_remover)

                # Devolve a quantidade ao estoque se for um produto físico
                if isinstance(item_removido, ProdutoFisico):
                    produto_original_no_mercado = self._produtos.get(item_removido.id)
                    produto_original_no_mercado.quantidade += item_removido.quantidade
                    self.salvar_produtos()
                
                console.print(f"\n[green]Item '{item_removido.nome}' removido do pedido com sucesso![/]")
            elif escolha == "3":
                if not novo_pedido.produtos:
                    console.print("\n[bold yellow]Pedido cancelado pois o carrinho está vazio.[/]")
                    break

                novo_pedido.status = 'aguardando entrega'
                self._pedidos.append(novo_pedido)
                self.salvar_pedidos()
                
                console.print(f"\n[bold green]Pedido nº {novo_pedido.id} concluído com sucesso![/]")
                console.print(f"Status atual: [cyan]{novo_pedido.status}[/]")
                break

    def selecionar_produto(self) -> int | None:
        """
        Exibe os produtos disponíveis, pede para o usuário selecionar um
        e retorna o ID do produto selecionado.

        Returns:
            O ID do produto selecionado ou None se não houver produtos.
        """
        self.exibir_produtos()
        if not self._produtos:
            # A mensagem de "nenhum produto" já é exibida por exibir_produtos()
            return None

        ids_validos = [str(id) for id in self._produtos.keys()]
        id_selecionado_str = Prompt.ask("\n[bold]Digite o ID do produto desejado[/]", choices=ids_validos)

        return int(id_selecionado_str)