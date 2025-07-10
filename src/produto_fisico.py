from produto import Produto
import hashlib

class ProdutoFisico(Produto):
    def __init__(self, id: int, nome: str, preco: float, quantidade: float, 
                 altura: float, largura: float, profundidade: float):
        """
        Inicializa um produto físico
        
        Args:
            id: Identificador único do produto
            nome: Nome do produto
            preco: Preço do produto
            quantidade: Quantidade em estoque
            altura: Altura do produto
            largura: Largura do produto
            profundidade: Profundidade do produto
        """
        super().__init__(id, nome, preco)
        self._quantidade = quantidade
        self._altura = altura
        self._largura = largura
        self._profundidade = profundidade
    
    def __str__(self):
            """
            Representação em string do produto físico
            """
            return (f"ProdutoFisico(id={self._id}, nome='{self._nome}', "
                    f"preco={self._preco}, quantidade={self._quantidade}, "
                    f"dimensoes={self._altura}x{self._largura}x{self._profundidade})")

    def calcular_estoque(self) -> float:
        """
        Calcula o estoque atual
        
        Returns:
            Quantidade em estoque
        """
        return self._quantidade
    
    def repor_estoque(self, quantidade: float) -> None:
        """
        Atualiza a quantidade em estoque
        
        Args:
            quantidade: Quantidade a ser adicionada ao estoque
        """
        self.quantidade += quantidade
    
    def calcular_volume(self) -> float:
        """
        Calcula o volume do produto
        
        Returns:
            Volume em unidades cúbicas
        """
        return self._altura * self._largura * self._profundidade
    
    def realizar_venda(self, quantidade: float) -> None:
        """
        Realiza uma venda do produto
        
        Args:
            quantidade: Quantidade a ser vendida
        """
        if quantidade > self._quantidade:
            raise ValueError("Quantidade insuficiente em estoque")
        
        self._quantidade -= quantidade

        # Retorna uma nova instância com a quantidade do pedido
        return ProdutoFisico(
            id=self._id,
            nome=self._nome,
            preco=self._preco,
            quantidade=quantidade,
            altura=self._altura,
            largura=self._largura,
            profundidade=self._profundidade
        )
    
    def calcular_frete(self, endereco_destino: str) -> float:
        """
        Calcula o custo do frete para o endereço de destino
        
        Args:
            endereco_destino: Endereço para onde o produto será enviado
        
        Returns:
            Custo estimado do frete
        """

        # Trata o endereço de destino
        if not endereco_destino or endereco_destino.strip() == "":
            raise ValueError("Endereço de destino não pode ser vazio")

        # Simula o cálculo do frete com base no endereço
        mn, mx = 10, 20; valor_deslocamento = mn + int(__import__('hashlib').sha256(endereco_destino.encode()).hexdigest(), 16) % (mx - mn + 1)

        volume_produto = self.calcular_volume()

        # Cálculo simples baseado no volume e deslocamento
        valor_frete = (volume_produto * 0.5) + valor_deslocamento

        return valor_frete
    
    def get_dic(self):
        """
        Retorna os dados do produto físico como um dicionário,
        incluindo os dados básicos da classe pai.
        """
        dados = super().get_dic()
        dados.update({
            "tipo": "fisico",
            "quantidade": self._quantidade,
            "altura": self._altura,
            "largura": self._largura,
            "profundidade": self._profundidade,
            "link_download": None
        })
        return dados