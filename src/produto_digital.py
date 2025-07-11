from produto import Produto
from rich.console import Console
from rich.prompt import Prompt, FloatPrompt

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
    
    # Getter
    @property
    def link_download(self) -> str:
        return self._link_download

    # Setter
    @link_download.setter
    def link_download(self, link: str):
        if not link or not link.strip():
            raise ValueError("O link de download não pode ser vazio.")
        self._link_download = link

    def __str__(self):
        """
        Representação em string do produto digital
        """
        return (f"ProdutoDigital(id={self.id}, nome='{self.nome}', "
                f"preco={self.preco}, link_download='{self.link_download}')")
    
    def realizar_venda(self):
        """
        Realiza a venda do produto digital
        
        Simula o processo de venda, como enviar o link de download ao cliente.
        """
        # Retorna uma nova instância do produto digital
        return ProdutoDigital(self.id, self.nome, self.preco, self.link_download)

    def get_dic(self):
        """
        Retorna os dados do produto digital como um dicionário,
        incluindo os dados básicos da classe pai.
        """
        dados = super().get_dic()
        dados.update({
            "tipo": "digital",
            "link_download": self.link_download,
            "quantidade": None,
            "altura": None,
            "largura": None,
            "profundidade": None
        })
        return dados

    def exibir_menu_edicao(self):
        """
        Exibe um menu interativo para editar os atributos do produto digital.
        """
        console = Console()
        
        while True:
            console.print(f"\nEditando: [bold cyan]{self.nome}[/]")
            console.print("\n[bold]O que você deseja editar?[/]")
            console.print("  [cyan]1.[/] Nome")
            console.print("  [cyan]2.[/] Preço")
            console.print("  [cyan]3.[/] Link de Download")
            console.print("  [cyan]4.[/] Concluir Edição")

            escolha = Prompt.ask("[bold]Escolha uma opção[/]", choices=["1", "2", "3", "4"])

            if escolha == "1":
                self.nome = Prompt.ask("Novo nome", default=self.nome)
            elif escolha == "2":
                self.preco = FloatPrompt.ask("Novo preço (R$)", default=self.preco)
            elif escolha == "3":
                self.link_download = Prompt.ask("Novo link de download", default=self.link_download)
            elif escolha == "4":
                break
            
            console.print("[green]Campo atualizado.[/]")