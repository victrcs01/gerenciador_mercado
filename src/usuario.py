from abc import ABC, abstractmethod

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
    
    def __str__(self):
        """
        Representação em string do usuário
        """
        return f"Usuario(id={self._id}, nome='{self._nome}', email='{self._email}')"
    
    def __repr__(self):
        """
        Representação para debug
        """
        return self.__str__()
    
    def get_dic(self):
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