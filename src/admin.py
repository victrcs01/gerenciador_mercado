from mercado import Mercado
from usuario import Usuario
from rich.console import Console
from rich.prompt import Prompt

class Admin(Usuario):
    """
    Classe que representa um usuário administrador do sistema
    """
    def __init__(self, id: int, nome: str, endereco: str, telefone: str, email: str, senha: str):
        """
        Inicializa um usuário administrador

        Args:
            id: ID do usuário
            nome: Nome do usuário
            endereco: Endereço do usuário
            telefone: Telefone do usuário
            email: E-mail do usuário
            senha: Senha do usuário
        """
        super().__init__(id, nome, endereco, telefone, email, senha, tipo='administrador')
    
    def __str__(self):
        """
        Representação em string do administrador
        """
        return f"Admin(id={self._id}, nome='{self._nome}', email='{self._email}')"

    def exibir_menu(self, mercado: Mercado):
        """
        Exibe o menu de opções para o administrador e gerencia a navegação.
        """
        console = Console()
        while True:
            console.print("\n[bold magenta]----- Menu do Administrador -----[/bold magenta]")
            console.print("[cyan]1.[/] Verificar Estoque")
            console.print("[cyan]2.[/] Cadastrar Produto")
            console.print("[cyan]3.[/] Editar Produto")
            console.print("[cyan]4.[/] Verificar Pedidos")
            console.print("[cyan]5.[/] Processar Pedido")
            console.print("[cyan]6.[/] Sair")

            escolha = Prompt.ask("[bold]Escolha uma opção[/]", choices=["1", "2", "3", "4", "5", "6"])

            if escolha == "1":
                mercado.exibir_produtos()
            elif escolha == "2":
                mercado.cadastrar_produto()
            elif escolha == "3":
                self._editar_produto()
            elif escolha == "4":
                self._verificar_pedidos()
            elif escolha == "5":
                self._processar_pedido()
            elif escolha == "6":
                console.print("\n[bold blue]Saindo do sistema. Até logo![/]")
                break
    
    # Métodos de espaço reservado (placeholders) para as funcionalidades do menu
    def _verificar_estoque(self):
        Console().print("\n[yellow]Funcionalidade 'Verificar Estoque' ainda não implementada.[/yellow]")
    def _cadastrar_produto(self):
        Console().print("\n[yellow]Funcionalidade 'Cadastrar Produto' ainda não implementada.[/yellow]")
    def _editar_produto(self):
        Console().print("\n[yellow]Funcionalidade 'Editar Produto' ainda não implementada.[/yellow]")
    def _verificar_pedidos(self):
        Console().print("\n[yellow]Funcionalidade 'Verificar Pedidos' ainda não implementada.[/yellow]")
    def _processar_pedido(self):
        Console().print("\n[yellow]Funcionalidade 'Processar Pedido' ainda não implementada.[/yellow]")
        
    
