from produto import Produto

class ProdutoDigital(Produto):
    def __init__(self, id: int, nome: str, preco: float, link_download: str):
        """
        Inicializa um produto digital
        
        Args:
            id: Identificador único do produto
            nome: Nome do produto
            preco: Preço do produto
            link_download: Link para download do produto
        """
        super().__init__(id, nome, preco)
        self._link_download = link_download
    
    def gerar_link_download(self) -> str:
        """
        Gera ou retorna o link de download
        
        Returns:
            Link para download do produto
        """
        return self._link_download
    
    def __str__(self):
        """
        Representação em string do produto digital
        """
        return (f"ProdutoDigital(id={self._id}, nome='{self._nome}', "
                f"preco={self._preco}, link_download='{self._link_download}')")
    
    def realizar_venda(self):
        """
        Realiza a venda do produto digital
        
        Simula o processo de venda, como enviar o link de download ao cliente.
        """
        # Retorna uma nova instância do produto digital
        return ProdutoDigital(self._id, self._nome, self._preco, self._link_download)

    def get_dic(self):
        """
        Retorna os dados do produto digital como um dicionário,
        incluindo os dados básicos da classe pai.
        """
        dados = super().get_dic()
        dados.update({
            "tipo": "digital",
            "link_download": self._link_download,
            "quantidade": None,
            "altura": None,
            "largura": None,
            "profundidade": None
        })
        return dados