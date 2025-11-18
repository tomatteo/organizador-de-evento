class Local:
    def __init__(self, id: int, nome: str, endereco: str, capacidade: int):
        self._id = id
        self._nome = nome
        self._endereco = endereco
        self._capacidade = capacidade
    
    @property
    def nome(self) -> str: return self._nome
    
    @property
    def endereco(self) -> str: return self._endereco

    def __str__(self):
        return f"Local: {self.nome} ({self.endereco})"