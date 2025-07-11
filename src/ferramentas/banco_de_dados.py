import pandas as pd
import os

class BancoDeDados:
    def __init__(self):
        """
        Inicializa a calsse com o caminho do diretório data
        """
        self._caminho_diretorio = os.path.join(os.getcwd(), "data")
        
        # Cria o diretório data se não existir
        if not os.path.exists(self._caminho_diretorio):
            os.makedirs(self._caminho_diretorio)
    
    def salvar_tabela(self, dados: pd.DataFrame, nome_tabela: str) -> None:
        """
        Salva uma tabela em arquivo Excel
        
        Args:
            dados: DataFrame com os dados a serem salvos
            nome_tabela: Nome da tabela (sem extensão, usa .xlsx por padrão)
        """
        
        # Adiciona extensão .xlsx se não tiver
        if not nome_tabela.endswith('.xlsx'):
            nome_tabela += '.xlsx'
        
        caminho_arquivo = os.path.join(self._caminho_diretorio, nome_tabela)
        
        # Salva o DataFrame em Excel
        dados.to_excel(caminho_arquivo, index=False)
        
    
    def carregar_tabela(self, nome_tabela: str) -> pd.DataFrame:
        """
        Carrega uma tabela de um arquivo Excel
        
        Args:
            nome_tabela: Nome do arquivo Excel a ser carregado
            
        Returns:
            DataFrame com os dados carregados
        """
        # Adiciona extensão .xlsx se não tiver
        if not nome_tabela.endswith('.xlsx'):
            nome_tabela += '.xlsx'
        
        caminho_arquivo = os.path.join(self._caminho_diretorio, nome_tabela)
        
        if not os.path.exists(caminho_arquivo):
            return pd.DataFrame()
        
        # Carrega o arquivo Excel
        df = pd.read_excel(caminho_arquivo)
        
        return df