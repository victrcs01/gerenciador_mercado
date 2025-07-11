from abc import ABC
from rich.console import Console
from rich.table import Table

from produto_digital import ProdutoDigital
from produto_fisico import ProdutoFisico

class ExibirProdutos(ABC):
    def __init__(self, produtos=None):
        """
        Inicializa a classe para exibir produtos disponíveis no mercado.
        """
        self._produtos = produtos
        
    def exibir_produtos(self):
        """
        Exibe os produtos disponíveis no mercado ou no pedido em uma tabela formatada.
        """
        console = Console()
        tabela = Table(title="Produtos", show_header=True, header_style="bold magenta")

        tabela.add_column("ID", style="dim", width=6, justify="center")
        tabela.add_column("Nome", min_width=20)
        tabela.add_column("Quantidade", justify="center")
        tabela.add_column("Preço (R$)", justify="right")

        if not self._produtos:
            console.print("[yellow]Nenhum produto adicionado.[/yellow]")
            return

        # Lida com dicionários (do Mercado) e listas (do Pedido)
        produtos_iteraveis = self._produtos.values() if isinstance(self._produtos, dict) else self._produtos

        for produto in produtos_iteraveis:
            if isinstance(produto, ProdutoFisico):
                quantidade_str = str(produto.quantidade)
            elif isinstance(produto, ProdutoDigital):
                quantidade_str = "[cyan]Digital[/cyan]"
            else:
                quantidade_str = "N/A"

            tabela.add_row(str(produto.id), produto.nome, quantidade_str, f"{produto.preco:.2f}")
        
        console.print("\n", tabela)