import pandas as pd
import os

class BancoDeDados:
    def __init__(self):
        """
        Inicializa a calsse com o caminho do diretório data
        """
        self.caminho_diretorio = os.path.join(os.getcwd(), "data")
        
        # Cria o diretório data se não existir
        if not os.path.exists(self.caminho_diretorio):
            os.makedirs(self.caminho_diretorio)
    
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
        
        caminho_arquivo = os.path.join(self.caminho_diretorio, nome_tabela)
        
        # Salva o DataFrame em Excel
        dados.to_excel(caminho_arquivo, index=False)
        
        print(f"Tabela '{nome_tabela}' salva em: {caminho_arquivo}")
    
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
        
        caminho_arquivo = os.path.join(self.caminho_diretorio, nome_tabela)
        
        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
        
        # Carrega o arquivo Excel
        df = pd.read_excel(caminho_arquivo)
        
        print(f"Tabela carregada de: {caminho_arquivo}")
        return df


# Teste
if __name__ == "__main__":
    # Cria instância do banco de dados
    bd = BancoDeDados()
    
    # Dados de exemplo
    dados_usuarios = [
        {"id": 1, "nome": "João", "email": "joao@email.com"},
        {"id": 2, "nome": "Maria", "email": "maria@email.com"},
        {"id": 3, "nome": "Pedro", "email": "pedro@email.com"}
    ]
    
    # Recebe tabela
    bd.receber_tabela(dados_usuarios, "usuarios")
    
    # Salva tabela
    bd.salvar_tabela("usuarios")
    
    # Carrega tabela
    df_carregado = bd.carregar_tabela("usuarios")
    print("\nDados carregados:")
    print(df_carregado)