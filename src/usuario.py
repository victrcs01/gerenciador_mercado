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
    
    def exibir_dados(self) -> None:
        """
        Exibe os dados do usuário (sem mostrar a senha)
        """
        print(f"ID: {self._id}")
        print(f"Nome: {self._nome}")
        print(f"Tipo: {self._tipo}")
        print(f"Endereço: {self._endereco}")
        print(f"Telefone: {self._telefone}")
        print(f"E-mail: {self._email}")
        print(f"Senha: {'*' * len(self.senha)}")
    
    def alterar_senha(self, nova_senha: str) -> None:
        """
        Altera a senha do usuário
        
        Args:
            nova_senha: Nova senha
        """
        self.senha = nova_senha
        print("Senha alterada com sucesso!")
    
    def verificar_senha(self, senha: str) -> bool:
        """
        Verifica se a senha fornecida está correta
        
        Args:
            senha: Senha a ser verificada
            
        Returns:
            True se a senha estiver correta, False caso contrário
        """
        return self.senha == senha
    
    def atualizar_dados(self, nome: str = None, endereco: str = None, 
                       telefone: str = None, email: str = None) -> None:
        """
        Atualiza os dados do usuário
        
        Args:
            nome: Novo nome (opcional)
            endereco: Novo endereço (opcional)
            telefone: Novo telefone (opcional)
            email: Novo e-mail (opcional)
        """
        if nome is not None:
            self.nome = nome
        if endereco is not None:
            self.endereco = endereco
        if telefone is not None:
            self.telefone = telefone
        if email is not None:
            self.email = email
        
        print("Dados atualizados com sucesso!")
    
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