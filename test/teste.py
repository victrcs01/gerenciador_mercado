from time import sleep
from rich.console import Console
from rich.table   import Table
from rich.progress import Progress, track
from rich.prompt  import Prompt, Confirm

console = Console()

# 1. Texto colorido e com estilo
console.print("[bold magenta]Rich[/] permite [green]cores[/], [italic]itálico[/], "
              "e muitos outros efeitos! :sparkles:")

# 2. Usando marcação inline
console.print("Você também pode combinar [bold red]várias[/] marcas em uma só linha.")

# 3. Criando e mostrando uma tabela
tabela = Table(title="Planetas do Sistema Solar")

tabela.add_column("Nome", style="cyan", no_wrap=True)
tabela.add_column("Ordem", justify="right")
tabela.add_column("Diâmetro (km)", justify="right")

planetas = [
    ("Mercúrio", 1, "4 879"),
    ("Vênus",    2, "12 104"),
    ("Terra",    3, "12 742"),
    ("Marte",    4, "6 779"),
]

for nome, ordem, diam in planetas:
    tabela.add_row(nome, str(ordem), diam)

console.print(tabela)

# 4. Barra de progresso (modo manual)
console.print("\nAnalisando dados...")
with Progress() as progress:
    tarefa = progress.add_task("Processando", total=100)
    for _ in range(10):
        sleep(0.2)           # simula trabalho pesado
        progress.update(tarefa, advance=10)

# 4b. Barra de progresso simplificada com track()
console.print("\nBaixando arquivos:")
for _ in track(range(15), description="Baixando…"):
    sleep(0.1)

console.print("\n[bold green]Pronto![/]")


# Pergunta simples com estilo:
nome = Prompt.ask("[bold cyan]Qual é o seu nome?[/]")

# Pergunta com valor padrão e validação automática de opções:
cor = Prompt.ask(
    "[green]Escolha uma cor favorita[/]", 
    choices=["vermelho", "azul", "verde"], 
    default="azul"
)

# Pergunta “sim/não” estilizada:
gosta_de_rich = Confirm.ask("[magenta]Você curte a biblioteca Rich?[/]")

# Entrada de senha (eco desativado):
senha = Prompt.ask("[yellow]Digite uma senha[/]", password=True)

console.print("\n[bold green]Resumo:[/]")
console.print(f"Nome: {nome}, Cor: {cor}, Curte Rich: {gosta_de_rich}, Senha: {'*' * len(senha)}")