from participante import Participante
#from evento import Evento

class Ingresso:
    def __init__(self, id: int, tipo: str, preco: float, participante: 'Participante', evento: 'Evento'):
        self._id = id
        self._tipo = tipo
        self._preco = preco
        self._status = "Vendido"
        self._participante = participante
        self._evento = evento
    
    @property
    def id(self) -> int: return self._id
    
    @property
    def status(self) -> str: return self._status
    
    @property
    def participante(self) -> 'Participante': return self._participante
    
    @property
    def evento(self) -> 'Evento': return self._evento

    def validar(self) -> bool:
        print(f"Ingresso {self.id} validado para {self.participante.nome}.")
        self._status = "Utilizado"
        return True

    def cancelar(self):
        print(f"Ingresso {self.id} cancelado.")
        self._status = "Cancelado"

    def __str__(self):
        return f"Ingresso {self.id} ({self._tipo}) - {self.status}"