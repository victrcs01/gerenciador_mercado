from datetime import datetime
import json
from typing import List, Union
from rich.console import Console

from produto import Produto
from produto_digital import ProdutoDigital
from produto_fisico import ProdutoFisico
from exibir_produtos import ExibirProdutos

class Pedido(ExibirProdutos):
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
        self._data = data if data is not None else datetime.now()
        self._status = status
        super().__init__(produtos if produtos is not None else [])

    # Getters
    @property
    def id(self) -> int:
        return self._id

    @property
    def cliente_id(self) -> int:
        return self._cliente_id

    @property
    def data(self) -> datetime:
        return self._data

    @property
    def status(self) -> str:
        return self._status

    @property
    def produtos(self) -> List[Union[ProdutoDigital, ProdutoFisico]]:
        # Retorna uma cópia para proteger a lista interna de modificações externas diretas
        return self._produtos[:]

    # Setter
    @status.setter
    def status(self, novo_status: str):
        status_validos = ['pendente', 'aguardando entrega', 'entregue']
        if novo_status.lower() not in status_validos:
            raise ValueError(f"Status inválido. Use um dos seguintes: {', '.join(status_validos)}")
        self._status = novo_status.lower()

    def get_dic(self):
        """
        Retorna os dados do pedido como um dicionário para serialização.
        A lista de produtos é convertida para uma string JSON.
        """
        produtos_serializados = []
        for produto in self.produtos:
            item = {'id': produto.id}
            if isinstance(produto, ProdutoFisico):
                item['quantidade'] = produto.quantidade
            produtos_serializados.append(item)

        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'data': self.data.isoformat(),
            'status': self.status,
            'produtos': json.dumps(produtos_serializados)
        }

    def adicionar_produto(self, produto: Union[ProdutoDigital, ProdutoFisico]):
        """
        Adiciona um produto à lista de produtos do pedido.

        Args:
            produto (Union[ProdutoDigital, ProdutoFisico]): O produto a ser adicionado.
        """
        if not isinstance(produto, Produto):
            raise TypeError("O item adicionado deve ser uma instância de ProdutoDigital ou ProdutoFisico.")
        self._produtos.append(produto)
        Console().print(f"Produto '{produto.nome}' adicionado ao pedido.")

    def remover_produto_por_indice(self, indice: int) -> Union[ProdutoDigital, ProdutoFisico]:
        """
        Remove um produto da lista do pedido pelo seu índice.

        Args:
            indice (int): O índice do produto a ser removido.

        Returns:
            O produto que foi removido.
        """
        if not 0 <= indice < len(self._produtos):
            raise IndexError("Índice de remoção fora do intervalo.")
        return self._produtos.pop(indice)

    def calcular_total(self) -> float:
        """
        Calcula o valor total do pedido somando o preço de todos os produtos.

        Returns:
            float: O valor total do pedido.
        """
        total = 0.0
        for produto in self.produtos:
            if isinstance(produto, ProdutoFisico):
                # Para produtos físicos, o preço é multiplicado pela quantidade no pedido + frete
                total += ( produto.preco * produto.quantidade ) + produto.calcular_frete()
            else:
                # Para produtos digitais, o preço é fixo
                total += produto.preco
        return total

    def processar_entrega(self):
        """
        Processa a entrega dos produtos do pedido.
        Para produtos digitais, gera o link de download.
        Para produtos físicos, simula o envio.
        """
        console = Console()
        console.print(f"\n[bold blue]Processando entrega do Pedido #{self.id}...[/]")

        for produto in self.produtos:
            if isinstance(produto, ProdutoDigital):
                link = produto.link_download
                console.print(f"  - [green]Enviando link para '{produto.nome}':[/] {link}")
            elif isinstance(produto, ProdutoFisico):
                console.print(f"  - [green]Preparando envio de {produto.quantidade}x '{produto.nome}'...[/]")

        self.status = 'entregue'
        console.print(f"\n[bold green]Entrega processada com sucesso! Novo status do pedido: {self.status.title()}[/]")

    def __str__(self):
        return (f"Pedido(id={self.id}, cliente_id={self.cliente_id}, "
                f"status='{self.status}', total=R${self.calcular_total():.2f})")