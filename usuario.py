from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, id: int, nome: str, email: str, senha: str):
        self._id = id
        self._nome = nome
        self._email = email
        self._senha = senha
    
    @property
    def id(self) -> int: return self._id
    
    @property
    def nome(self) -> str: return self._nome
    
    @property
    def senha(self) -> str: return self._senha

    @property
    def email(self) -> str: return self._email



    @abstractmethod
    def autenticar(self, senha: str) -> bool:
        pass

    def __str__(self):
        return f"[{self.__class__.__name__}] {self.nome} ({self.email})"