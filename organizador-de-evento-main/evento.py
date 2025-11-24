from local import Local
from ingresso import Ingresso
from datetime import datetime

class Evento:
    def __init__(self, id: int, nome: str, descricao: str, dataInicio: datetime, dataFim: datetime, capacidade: int, local_info: dict):
        self._id = id
        self._nome = nome
        self._descricao = descricao
        self._dataInicio = dataInicio
        self._dataFim = dataFim
        self._capacidade = capacidade
        self._status = "Planejado"
        
        self._local = Local(
            id=local_info['id'],
            nome=local_info['nome'],
            endereco=local_info['endereco'],
            capacidade=local_info['capacidade']
        )
        
        self._ingressos: list[Ingresso] = []

    @property
    def nome(self) -> str: return self._nome
    
    @property
    def descricao(self) -> str:
        return self._descricao
    @property
    def local(self) -> Local: return self._local
    
    @property
    def ingressos(self) -> list[Ingresso]: return self._ingressos
    
    @property
    def capacidade(self) -> int: return self._capacidade
    
    @property
    def data_inicio(self):
        return self._dataInicio

    @property
    def data_fim(self):
        return self._dataFim

    def validarCapacidade(self) -> bool:
        vagas_ocupadas = len([ing for ing in self._ingressos if ing.status == "Vendido"])
        if vagas_ocupadas < self._capacidade:
            return True
        print(f"**REGRA DE NEGÓCIO (FALHA)**: Capacidade máxima do evento '{self.nome}' atingida ({self._capacidade}).")
        return False

    def adicionarIngresso(self, ingresso: Ingresso):
        if self.validarCapacidade():
            self._ingressos.append(ingresso)
            vagas_restantes = self.capacidade - len([ing for ing in self.ingressos if ing.status == "Vendido"])
            print(f"Ingresso adicionado ao evento '{self.nome}'. Vagas restantes: {vagas_restantes}")
        else:
            raise ValueError("Não foi possível adicionar ingresso, capacidade esgotada.")

    def __str__(self):
        vagas_ocupadas = len([ing for ing in self.ingressos if ing.status == "Vendido"])
        return (f"Evento: {self.nome} (Status: {self._status})\n"
                f"   Local: {self.local.nome}\n"
                f"   Vagas: {vagas_ocupadas}/{self.capacidade}")