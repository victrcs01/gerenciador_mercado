from datetime import datetime
from typing import List, Union

from produto import Produto
from produto_digital import ProdutoDigital
from produto_fisico import ProdutoFisico
from rich.console import Console


class Pedido:
    """
    Representa um pedido feito por um cliente no mercado.
    """

    def __init__(self, id: int, cliente_id: int, produtos: List[Union[ProdutoDigital, ProdutoFisico]] = None,
                 data: datetime = None, status: str = 'pendente'):
        """
        Inicializa um pedido.

        Args:
            id: O identificador único do pedido.
            cliente_id: O ID do cliente que fez o pedido.
            produtos: Lista de produtos no pedido. Defaults to None.
            data: A data em que o pedido foi feito. Defaults to datetime.now().
            status: O status atual do pedido. Defaults to 'pendente'.
        """
        self._id = id
        self._cliente_id = cliente_id
        self._produtos = produtos if produtos is not None else []
        self._data = data if data is not None else datetime.now()
        self._status = status

    def adicionar_produto(self, produto: Union[ProdutoDigital, ProdutoFisico]):
        """
        Adiciona um produto à lista de produtos do pedido.

        Args:
            produto (Union[ProdutoDigital, ProdutoFisico]): O produto a ser adicionado.
        """
        if not isinstance(produto, Produto):
            raise TypeError("O item adicionado deve ser uma instância de ProdutoDigital ou ProdutoFisico.")
        self._produtos.append(produto)
        Console().print(f"Produto '{produto._nome}' adicionado ao pedido.")

    def calcular_total(self) -> float:
        """
        Calcula o valor total do pedido somando o preço de todos os produtos.

        Returns:
            float: O valor total do pedido.
        """
        total = 0.0
        for produto in self._produtos:
            if isinstance(produto, ProdutoFisico):
                # Para produtos físicos, o preço é multiplicado pela quantidade no pedido
                total += produto._preco * produto._quantidade
            else:
                # Para produtos digitais, o preço é fixo
                total += produto._preco
        return total

    def processar_entrega(self):
        """
        Processa a entrega dos produtos do pedido.
        Para produtos digitais, gera o link de download.
        Para produtos físicos, simula o envio.
        """
        console = Console()
        console.print(f"\n[bold blue]Processando entrega do Pedido #{self._id}...[/]")

        for produto in self._produtos:
            if isinstance(produto, ProdutoDigital):
                link = produto.gerar_link_download()
                console.print(f"  - [green]Enviando link para '{produto._nome}':[/] {link}")
            elif isinstance(produto, ProdutoFisico):
                console.print(f"  - [green]Preparando envio de {produto._quantidade}x '{produto._nome}'...[/]")

        self._status = 'processado'
        console.print(f"[bold green]Entrega processada com sucesso! Novo status do pedido: {self._status}[/]")

    def __str__(self):
        return (f"Pedido(id={self._id}, cliente_id={self._cliente_id}, "
                f"status='{self._status}', total=R${self.calcular_total():.2f})")