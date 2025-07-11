from abc import ABC, abstractmethod

class Produto(ABC):
    def __init__(self, id: int, nome: str, preco: float):
        """
        Inicializa um produto
        
        Args:
            id: Identificador único do produto
            nome: Nome do produto
            preco: Preço do produto
        """
        self._id = id
        self._nome = nome
        self._preco = preco

    # Getters
    @property
    def id(self) -> int:
        return self._id

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def preco(self) -> float:
        return self._preco

    # Setters
    @nome.setter
    def nome(self, nome: str):
        self._nome = nome

    @preco.setter
    def preco(self, preco: float):
        if preco < 0:
            raise ValueError("O preço não pode ser negativo.")
        self._preco = preco
    
    def __str__(self):
        """
        Representação em string do produto
        """
        return f"Produto(id={self._id}, nome='{self._nome}', preco={self._preco})"
    
    def __repr__(self):
        """
        Representação para debug
        """
        return self.__str__()
    
    def get_dic(self):
        """
        Retorna os dados básicos do produto como um dicionário.
        """
        return {
            "id": self._id,
            "nome": self._nome,
            "preco": self._preco,
        }
    
    @abstractmethod
    def realizar_venda(self):
        """
        Método abstrato para realizar uma venda do produto
        """
        pass

    @abstractmethod
    def exibir_menu_edicao(self):
        """
        Exibe um menu interativo para editar os atributos do produto.
        """
        pass