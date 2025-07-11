from mercado import Mercado
from usuario import Usuario
from rich.console import Console
from rich.table import Table
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
                mercado.editar_produto()
            elif escolha == "4":
                self._verificar_pedidos(mercado)
            elif escolha == "5":
                self._processar_pedido(mercado)
            elif escolha == "6":
                console.print("\n[bold blue]Saindo do sistema. Até logo![/]")
                break
    
    def _verificar_pedidos(self, mercado: Mercado):
        """
        Busca e exibe todos os pedidos do sistema.
        """
        console = Console()
        console.print("\n[bold yellow]----- Todos os Pedidos do Sistema -----[/bold yellow]")

        todos_os_pedidos = mercado.carregar_pedidos()

        if not todos_os_pedidos:
            console.print("Nenhum pedido foi realizado no sistema ainda.")
            return

        tabela = Table(show_header=True, header_style="bold magenta")
        tabela.add_column("ID Pedido", style="dim", justify="center")
        tabela.add_column("ID Cliente", justify="center")
        tabela.add_column("Data", justify="center")
        tabela.add_column("Status", justify="center")
        tabela.add_column("Total (R$)", justify="right")

        for pedido in todos_os_pedidos:
            status_cor = {"aguardando entrega": "yellow", "entregue": "green"}.get(pedido.status, "white")
            tabela.add_row(
                str(pedido.id),
                str(pedido.cliente_id),
                pedido.data.strftime("%d/%m/%Y %H:%M"),
                f"[{status_cor}]{pedido.status.replace('_', ' ').title()}[/]",
                f"{pedido.calcular_total():.2f}"
            )
        
        console.print(tabela)

    def _processar_pedido(self, mercado: Mercado):
        """
        Exibe os pedidos aguardando entrega e permite ao admin processá-los.
        """
        console = Console()
        console.print("\n[bold yellow]----- Processar Pedidos Pendentes -----[/bold yellow]")

        # Carrega todos os pedidos e filtra os que estão aguardando entrega
        todos_os_pedidos = mercado.carregar_pedidos()
        pedidos_pendentes = [p for p in todos_os_pedidos if p.status == 'aguardando entrega']

        if not pedidos_pendentes:
            console.print("Não há pedidos aguardando entrega no momento.")
            return

        tabela = Table(show_header=True, header_style="bold magenta")
        tabela.add_column("ID Pedido", style="dim", justify="center")
        tabela.add_column("ID Cliente", justify="center")
        tabela.add_column("Data", justify="center")
        tabela.add_column("Total (R$)", justify="right")

        ids_validos = []
        for pedido in pedidos_pendentes:
            ids_validos.append(str(pedido.id))
            tabela.add_row(
                str(pedido.id),
                str(pedido.cliente_id),
                pedido.data.strftime("%d/%m/%Y %H:%M"),
                f"{pedido.calcular_total():.2f}"
            )
        
        console.print(tabela)

        id_selecionado_str = Prompt.ask("\n[bold]Digite o ID do pedido que deseja processar[/]", choices=ids_validos)
        id_selecionado = int(id_selecionado_str)

        # Encontra o pedido selecionado na lista original para modificar
        pedido_a_processar = next((p for p in todos_os_pedidos if p.id == id_selecionado), None)

        if pedido_a_processar:
            pedido_a_processar.processar_entrega()
            mercado.salvar_pedidos()
