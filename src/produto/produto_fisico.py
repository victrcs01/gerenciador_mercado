from produto.produto import Produto
import hashlib
from rich.console import Console
from rich.prompt import Prompt, FloatPrompt, IntPrompt

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

    # Getters
    @property
    def quantidade(self) -> float:
        return self._quantidade

    @property
    def altura(self) -> float:
        return self._altura

    @property
    def largura(self) -> float:
        return self._largura

    @property
    def profundidade(self) -> float:
        return self._profundidade

    # Setters
    @quantidade.setter
    def quantidade(self, quantidade: float):
        if quantidade < 0:
            raise ValueError("A quantidade não pode ser negativa.")
        self._quantidade = quantidade

    @altura.setter
    def altura(self, altura: float):
        if altura <= 0:
            raise ValueError("A altura deve ser um valor positivo.")
        self._altura = altura

    @largura.setter
    def largura(self, largura: float):
        if largura <= 0:
            raise ValueError("A largura deve ser um valor positivo.")
        self._largura = largura
    
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
        self.quantidade += quantidade # Usa o setter implicitamente
    
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
        
        self.quantidade -= quantidade # Usa o setter implicitamente

        # Retorna uma nova instância com a quantidade do pedido
        return ProdutoFisico(
            id=self.id,
            nome=self.nome,
            preco=self.preco,
            quantidade=quantidade,
            altura=self._altura,
            largura=self._largura,
            profundidade=self._profundidade
        )
    
    def calcular_frete(self) -> float:
        """
        Calcula o custo do frete para o endereço de destino
        
        Args:
            endereco_destino: Endereço para onde o produto será enviado
        
        Returns:
            Custo estimado do frete
        """

        # Simula o cálculo do frete com base no endereço
        volume_produto = self.calcular_volume()

        # Cálculo simples baseado no volume
        valor_frete = (volume_produto * 0.5)

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

    def exibir_menu_edicao(self):
        """
        Exibe um menu interativo para editar os atributos do produto físico.
        """
        console = Console()

        while True:
            console.print(f"\nEditando: [bold cyan]{self.nome}[/]")
            console.print("\n[bold]O que você deseja editar?[/]")
            opcoes = {
                "1": "Nome", 
                "2": "Preço", 
                "3": "Quantidade", 
                "4": "Altura (cm)", 
                "5": "Largura (cm)", 
                "6": "Profundidade (cm)"
            }
            for key, value in opcoes.items():
                console.print(f"  [cyan]{key}.[/] {value}")
            
            sair_opcao = str(len(opcoes) + 1)
            console.print(f"  [cyan]{sair_opcao}.[/] Concluir Edição")

            escolha = Prompt.ask("[bold]Escolha uma opção[/]", choices=[*opcoes.keys(), sair_opcao])

            if escolha == sair_opcao:
                break
            
            campo = opcoes[escolha]
            if campo == "Nome":
                self.nome = Prompt.ask("Novo nome", default=self.nome)
            elif campo == "Preço":
                self.preco = FloatPrompt.ask("Novo preço (R$)", default=self.preco)
            elif campo == "Quantidade":
                self.quantidade = IntPrompt.ask("Nova quantidade", default=self.quantidade)
            elif campo == "Altura (cm)":
                self.altura = FloatPrompt.ask("Nova altura", default=self.altura)
            elif campo == "Largura (cm)":
                self.largura = FloatPrompt.ask("Nova largura", default=self.largura)
            elif campo == "Profundidade (cm)":
                self.profundidade = FloatPrompt.ask("Nova profundidade", default=self.profundidade)
            
            console.print("[green]Campo atualizado.[/]")