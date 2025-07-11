from abc import ABC, abstractmethod
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from mercado.mercado import Mercado

class Usuario:
    def __init__(self, id: int, nome: str, endereco: str, telefone: str, email: str, senha: str, tipo: str = 'cliente'):
        """
        Inicializa um usuário
        
        Args:
            id: Identificador único do usuário
            nome: Nome do usuário
            endereco: Endereço do usuário
            telefone: Telefone do usuário
            email: E-mail do usuário
            senha: Senha do usuário
            tipo: Tipo de usuário (padrão é 'cliete')
        """
        self._id = id
        self._nome = nome
        self._endereco = endereco
        self._telefone = telefone
        self._email = email
        self._senha = senha
        self._tipo = tipo  

    # Getters
    @property
    def id(self) -> int:
        """Identificador único (somente leitura)."""
        return self._id

    @property
    def nome(self) -> str:
        """Nome do usuário."""
        return self._nome

    @property
    def endereco(self) -> str:
        """Endereço do usuário."""
        return self._endereco

    @property
    def telefone(self) -> str:
        """Telefone do usuário."""
        return self._telefone

    @property
    def email(self) -> str:
        """E-mail do usuário."""
        return self._email

    @property
    def tipo(self) -> str:
        """Tipo de usuário (cliente, admin, etc.)."""
        return self._tipo
    
    # Senha não tem getter, pois não deve ser acessada diretamente
    
    def verificar_senha(self, senha: str) -> bool:
        """
        Verifica se a senha fornecida está correta
        
        Args:
            senha: Senha a ser verificada
            
        Returns:
            True se a senha estiver correta, False caso contrário
        """
        return self._senha == senha
    
    def __str__(self) -> str:
        """
        Representação em string do usuário
        """
        return f"Usuario(id={self._id}, nome='{self._nome}', email='{self._email}')"
    
    def __repr__(self) -> str:
        """
        Representação para debug
        """
        return self.__str__()
    
    def get_dic(self) -> dict:
        """
        Retorna os dados do usuário como um dicionário
        """
        return {
            "id": self._id,
            "nome": self._nome,
            "endereco": self._endereco,
            "telefone": self._telefone,
            "email": self._email,
            "senha": self._senha,
            "tipo": self._tipo
        }

    def exibir_menu(self, mercado: Mercado):
        """
        Exibe o menu de opções para o cliente e gerencia a navegação.

        Args:
            mercado: A instância da classe Mercado para interagir com produtos e pedidos.
        """
        console = Console()
        while True:
            console.print("\n[bold magenta]----- Menu do Cliente -----[/bold magenta]")
            console.print("[cyan]1.[/] Verificar meus Pedidos")
            console.print("[cyan]2.[/] Fazer Novo Pedido")
            console.print("[cyan]3.[/] Sair")

            escolha = Prompt.ask("[bold]Escolha uma opção[/]", choices=["1", "2", "3"])

            if escolha == "1":
                self._verificar_pedidos(mercado)
            elif escolha == "2":
                mercado.fazer_novo_pedido(self._id)
            elif escolha == "3":
                console.print("\n[bold blue]Saindo do sistema. Até logo![/]")
                break

    def _verificar_pedidos(self, mercado: Mercado):
        """
        Busca e exibe os pedidos associados a este usuário.
        """
        console = Console()
        console.print("\n[bold yellow]----- Meus Pedidos -----[/bold yellow]")

        pedidos_do_cliente = mercado.carregar_pedidos(cliente_id=self.id)

        if not pedidos_do_cliente:
            console.print("Você ainda não fez nenhum pedido.")
            return

        tabela = Table(show_header=True, header_style="bold magenta")
        tabela.add_column("ID Pedido", style="dim", justify="center")
        tabela.add_column("Data", justify="center")
        tabela.add_column("Status", justify="center")
        tabela.add_column("Nº de Itens", justify="center")
        tabela.add_column("Total (R$)", justify="right")

        for pedido in pedidos_do_cliente:
            status_cor = {"aguardando entrega": "yellow", "entregue": "green"}.get(pedido.status, "white")
            
            tabela.add_row(
                str(pedido.id),
                pedido.data.strftime("%d/%m/%Y %H:%M"),
                f"[{status_cor}]{pedido.status.replace('_', ' ').title()}[/]",
                str(len(pedido.produtos)),
                f"{pedido.calcular_total():.2f}"
            )
        
        console.print(tabela)