from usuario import Usuario

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
        super().__init__(id, nome, endereco, telefone, email, senha)

        # Carrega os dados do mercado
        self._mercado = None
    
    def __str__(self):
        """
        Representação em string do administrador
        """
        return f"Admin(id={self._id}, nome='{self._nome}', email='{self._email}')"
    
