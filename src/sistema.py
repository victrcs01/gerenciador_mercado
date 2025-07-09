from banco_de_dados import BancoDeDados
from mercado import Mercado

class Sistema:

    def __init__(self):
        """
        Inicializa o sistema de gerenciamento de mercado, carregando os dados
        """ 
        self._usuarios = self.carregar_usuarios()
        self.mercado = self.carregar_mercado()

    def carregar_usuarios(self):
        """
        Carrega os usuários do sistema a partir do banco de dados
        """
        return BancoDeDados().carregar_tabela('usuarios')