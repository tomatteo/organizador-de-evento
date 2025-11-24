# organizador.py
from usuario import Usuario
from evento import Evento
#from ingresso import Ingresso // Para acessar o método cancelar() do Ingresso
from typing import Union # precisa disso pra corrigir o TypeError

class Organizador(Usuario):
    def __init__(self, id: int, nome: str, email: str, senha: str, verificado: bool = False):
        super().__init__(id, nome, email, senha)
        self._verificado = verificado

    @property
    def verificado(self) -> bool: return self._verificado

    def autenticar(self, senha: str) -> bool:
        is_valid = (self._senha == senha)
        if not self._verificado:
            print(f"Autenticação (Organizador) para {self.nome}: Falha (Conta não verificada)")
            return False
            
        print(f"Autenticação (Organizador) para {self.nome}: {'Sucesso' if is_valid else 'Falha'}")
        return is_valid
    
    def criarEvento(self, id: int, nome: str, desc: str, dt_inicio, dt_fim, cap: int, local_info: dict) -> Union[Evento, None]:
        if not self.verificado:
            print(f"Organizador {self.nome} não pode criar eventos (Não verificado).")
            return None
        
        print(f"Organizador {self.nome} criando evento '{nome}'...")
        # classe Evento lida com o datetime internamente não precisa importar aqui.
        novo_evento = Evento(
            id=id, nome=nome, descricao=desc, 
            dataInicio=dt_inicio, dataFim=dt_fim, 
            capacidade=cap, local_info=local_info
        )
        return novo_evento

    def editarEvento(self, evento: Evento, novo_nome: str):
        print(f"Organizador {self.nome} editando evento '{evento.nome}'.")
        evento._nome = novo_nome

    def cancelarEvento(self, evento: Evento):
        print(f"Organizador {self.nome} cancelando evento '{evento.nome}'.")
        evento._status = "Cancelado"
        for ingresso in evento.ingressos:
            if ingresso.status == "Vendido":
                ingresso.cancelar()