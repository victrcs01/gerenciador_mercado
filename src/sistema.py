import re
import pandas as pd
from banco_de_dados import BancoDeDados
from mercado import Mercado
from usuario import Usuario
from rich.console import Console
from rich.prompt import Prompt

class Sistema:

    def __init__(self):
        """
        Inicializa o sistema de gerenciamento de mercado, carregando os dados
        """ 
        self._usuario_logado = None
        self.carregar_usuarios()
        #self.mercado = self.carregar_mercado()

    def carregar_usuarios(self):
        """
        Carrega os usuários do sistema a partir do banco de dados
        """

        # Carrega os dados do banco de dados
        tabela_usuarios = BancoDeDados().carregar_tabela("usuarios")

        # Loop em cada linha da tabela, criando uma instância de usuário
        lista_usuarios = [
            Usuario(id=row.id, nome=row.nome, email=row.email, senha=row.senha, endereco=row.endereco, telefone=row.telefone, tipo=row.tipo)
            for row in tabela_usuarios.itertuples(index=False)
        ]

        self._usuarios = lista_usuarios

    def salvar_usuarios(self):
        """
        Salva os dados dos usuários no banco de dados
        """
        
        # Converte as instâncias de usuário em um DataFrame
        dados_usuarios = pd.DataFrame([dado.get_dic() for dado in self._usuarios])
        # Salva os dados no banco de dado
        BancoDeDados().salvar_tabela(dados_usuarios, "usuarios")
    
    def cadastrar_admin(self):
        """
        Cadastra um usuário administrador no sistema
        """
        return self.cadastrar_usuario(tipo_usuario='administrador')

    def cadastrar_usuario(self, tipo_usuario='cliente'):
        """
        Realiza o primeiro acesso ao sistema, criando um usuário administrador
        """
        console = Console()
        console.print("[bold yellow]Primeiro acesso ao sistema![/]")
        console.print("[cyan]Por favor, preencha os dados do usuário administrador:\n[/]")

        # Função para validar nome
        def validar_nome(nome):
            if len(nome.strip()) < 2:
                return False, "Nome deve ter pelo menos 2 caracteres"
            if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', nome.strip()):
                return False, "Nome deve conter apenas letras e espaços"
            return True, ""

        # Função para validar endereço
        def validar_endereco(endereco):
            if len(endereco.strip()) < 10:
                return False, "Endereço deve ter pelo menos 10 caracteres"
            return True, ""

        # Função para validar telefone
        def validar_telefone(telefone):
            # Remove caracteres não numéricos
            telefone_limpo = re.sub(r'[^\d]', '', telefone)
            
            # Verifica se tem 10 ou 11 dígitos (telefone fixo ou celular)
            if len(telefone_limpo) not in [10, 11]:
                return False, "Telefone deve ter 10 ou 11 dígitos"
            
            # Verifica se começa com código de área válido (11-99)
            if not telefone_limpo[:2].isdigit() or int(telefone_limpo[:2]) < 11:
                return False, "Código de área deve ser entre 11 e 99"
            
            return True, ""

        # Função para validar email
        def validar_email(email):
            padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(padrao_email, email):
                return False, "Email deve ter formato válido (exemplo@dominio.com)"
            return True, ""

        # Função para validar senha
        def validar_senha(senha):
            erros = []
            
            if len(senha) < 8:
                erros.append("pelo menos 8 caracteres")
            if not re.search(r'[A-Z]', senha):
                erros.append("pelo menos uma letra maiúscula")
            if not re.search(r'[a-z]', senha):
                erros.append("pelo menos uma letra minúscula")
            if not re.search(r'\d', senha):
                erros.append("pelo menos um número")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
                erros.append("pelo menos um caractere especial")
            
            if erros:
                return False, f"Senha deve conter: {', '.join(erros)}"
            return True, ""

        # Coleta e validação do nome
        while True:
            nome = Prompt.ask("[bold cyan]Nome completo[/]").strip()
            valido, erro = validar_nome(nome)
            if valido:
                break
            console.print(f"[bold red]Erro: {erro}[/]")

        # Coleta e validação do endereço
        while True:
            endereco = Prompt.ask("[bold cyan]Endereço completo[/]").strip()
            valido, erro = validar_endereco(endereco)
            if valido:
                break
            console.print(f"[bold red]Erro: {erro}[/]")

        # Coleta e validação do telefone
        while True:
            telefone = Prompt.ask("[bold cyan]Telefone (com DDD)[/]").strip()
            valido, erro = validar_telefone(telefone)
            if valido:
                # Formatar o telefone para exibição
                telefone_limpo = re.sub(r'[^\d]', '', telefone)
                if len(telefone_limpo) == 11:
                    telefone_formatado = f"({telefone_limpo[:2]}) {telefone_limpo[2:7]}-{telefone_limpo[7:]}"
                else:
                    telefone_formatado = f"({telefone_limpo[:2]}) {telefone_limpo[2:6]}-{telefone_limpo[6:]}"
                break
            console.print(f"[bold red]Erro: {erro}[/]")

        # Coleta e validação do email
        while True:
            email = Prompt.ask("[bold cyan]Email[/]").strip().lower()
            valido, erro = validar_email(email)
            if valido:
                break
            console.print(f"[bold red]Erro: {erro}[/]")

        # Coleta e validação da senha
        while True:
            console.print("[dim]Requisitos da senha: mínimo 8 caracteres, pelo menos 1 maiúscula, 1 minúscula, 1 número e 1 caractere especial[/]")
            senha = Prompt.ask("[bold cyan]Senha[/]", password=True)
            valido, erro = validar_senha(senha)
            if valido:
                # Confirmação da senha
                confirmacao = Prompt.ask("[bold cyan]Confirme a senha[/]", password=True)
                if senha == confirmacao:
                    break
                else:
                    console.print("[bold red]Erro: As senhas não coincidem[/]")
            else:
                console.print(f"[bold red]Erro: {erro}[/]")

        # Salva a instância de usuários na memória
        instancia_usuario = Usuario(
            id=len(self._usuarios) + 1,
            nome=nome,
            endereco=endereco,
            telefone=telefone,
            email=email,
            senha=senha,
            tipo=tipo_usuario
        )
        self._usuarios.append(instancia_usuario)

        # Salva os dados no banco de dados
        self.salvar_usuarios()

        # Exibe resumo dos dados inseridos
        console.print("\n[bold green]Usuário cadastrado com sucesso![/]")
        console.print(f"[cyan]Nome:[/] {nome}")
        console.print(f"[cyan]Endereço:[/] {endereco}")
        console.print(f"[cyan]Telefone:[/] {telefone_formatado}")
        console.print(f"[cyan]Email:[/] {email}")
        console.print(f"[cyan]Senha:[/] {'*' * len(senha)}")
        
        return instancia_usuario

    def primeiro_acesso(self):
        """
        Realiza o primeiro acesso ao sistema, criando um usuário administrador
        """
        console = Console()
        
        # Aqui você pode implementar a lógica para criar um usuário administrador
        usuario_admin = self.cadastrar_usuario(tipo_usuario='administrador')

        # Define o usuário logado como o administrador criado, para não precisar fazer login novamente
        self._usuario_logado = usuario_admin  

        # Exemplo: solicitar dados do usuário e salvar no banco de dados
        console.print("[bold green]Usuário administrador criado com sucesso![/]")


    def login(self):
        """
        Realiza o login do usuário no sistema.
        Retorna o objeto do usuário se o login for bem-sucedido, caso contrário, None.
        """
        console = Console()
        console.print("\n[bold]----- Login no Sistema -----[/]")
        
        for _ in range(3):  # Permite 3 tentativas de login
            email = Prompt.ask("[cyan]Digite seu e-mail[/]").lower().strip()

            # Procura o usuário pelo e-mail na lista de usuários carregados
            usuario_encontrado = next((u for u in self._usuarios if u._email.lower() == email), None)

            if not usuario_encontrado:
                console.print("[bold red]E-mail não encontrado. Tente novamente.[/]\n")
                continue

            senha = Prompt.ask("[cyan]Digite sua senha[/]", password=True)

            if usuario_encontrado.verificar_senha(senha):
                console.print(f"\n[bold green]Login bem-sucedido! Bem-vindo(a), {usuario_encontrado._nome}![/]")
                self._usuario_logado = usuario_encontrado
                return self._usuario_logado
            else:
                console.print("[bold red]Senha incorreta. Tente novamente.[/]\n")

        console.print("[bold red]Número máximo de tentativas de login atingido. Retornando ao menu principal.[/]")
        return None

    def iniciar_sistema(self):
        """
        Inicia o sistema de gerenciamento de mercado, exibindo o menu inicial.
        """
        console = Console()
        console.print("[bold green]Bem-vindo ao Sistema de Gerenciamento de Mercado![/]")

        if not self._usuarios:
            console.print("\n[bold red]Nenhum usuário cadastrado. Realize o 'Primeiro Acesso' para criar o administrador.[/]")
            self.primeiro_acesso()  
        
        while True and not self._usuario_logado:
            console.print("\n[bold]----- Menu Inicial -----[/]")
            console.print("[cyan]1.[/] Primeiro Acesso")
            console.print("[cyan]2.[/] Realizar Login")
            console.print("[cyan]3.[/] Sair")

            escolha = Prompt.ask("\n[bold]Escolha uma opção[/]", choices=["1", "2", "3"], default="2")

            # Primeiro acesso -> Cria um usuário do cliente
            if escolha == "1":
                self.cadastrar_usuario()

            elif escolha == "2":

                if self.login():
                    # Login bem-sucedido, sai do loop do menu inicial
                    break
                # Se o login falhar, o método login() já informou o usuário e o loop continua.

            elif escolha == "3":
                console.print("\n[bold blue]Saindo do sistema. Até logo![/]")
                return  # Encerra o programa

        # --- Esta parte só é executada após um login bem-sucedido ---
        if self._usuario_logado:
            console.print("\n[bold cyan]Você está no menu principal do sistema.[/]")
            # Exemplo de como você poderia direcionar o usuário:
            # if self._usuario_logado.tipo == 'administrador':
            #     self.menu_admin()
            # else:
            #     self.menu_cliente()

def main():
    sistema = Sistema()
    sistema.iniciar_sistema()

if __name__ == "__main__":
    main()

       