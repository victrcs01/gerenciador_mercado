import pandas as pd
from banco_de_dados import BancoDeDados
from produto_digital import ProdutoDigital
from produto_fisico import ProdutoFisico
from rich.console import Console
from rich.prompt import Prompt, FloatPrompt, IntPrompt
from rich.table import Table

class Mercado:

    def __init__(self):
        """
        Inicializa o mercado com uma lista de produtos e pedidos
        """
        self._produtos = self.carregar_produtos()
        self._pedidos = []

    def carregar_produtos(self):
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

    def exibir_produtos(self):
        """
        Exibe os produtos disponíveis no mercado em uma tabela formatada.
        """
        console = Console()
        tabela = Table(title="Produtos Disponíveis", show_header=True, header_style="bold magenta")

        tabela.add_column("ID", style="dim", width=6, justify="center")
        tabela.add_column("Nome", min_width=20)
        tabela.add_column("Quantidade", justify="center")
        tabela.add_column("Preço (R$)", justify="right")

        if not self._produtos:
            console.print("[yellow]Nenhum produto cadastrado no mercado.[/yellow]")
            return

        for produto in self._produtos.values():
            if isinstance(produto, ProdutoFisico):
                quantidade_str = str(produto._quantidade)
            elif isinstance(produto, ProdutoDigital):
                quantidade_str = "[cyan]Digital[/cyan]"
            else:
                quantidade_str = "N/A"

            tabela.add_row(str(produto._id), produto._nome, quantidade_str, f"{produto._preco:.2f}")

        console.print(tabela)

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