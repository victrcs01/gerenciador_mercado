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
    
    @abstractmethod
    def realizar_venda(self):
        """
        Método abstrato para realizar uma venda do produto
        """
        pass