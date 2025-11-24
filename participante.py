from usuario import Usuario
# from ingresso import Ingresso
from typing import Union
#from evento import Evento

class Participante(Usuario):
    def __init__(self, id: int, nome: str, email: str, senha: str, cpf: str):
        super().__init__(id, nome, email, senha)
        self._cpf = cpf
        self._ingressos: list['Ingresso'] = []
    
    @property
    def cpf(self) -> str: return self._cpf
    
    @property
    def ingressos(self) -> list['Ingresso']: return self._ingressos

    def autenticar(self, senha: str) -> bool:
        is_valid = self._senha == senha
        print(f"Autenticação (Participante) para {self.nome}: {'Sucesso' if is_valid else 'Falha'}")
        return is_valid

    def inscreverEvento(self, evento: 'Evento', id_ingresso: int, tipo: str, preco: float) -> Union['Ingresso', None]: 
        print(f"Participante {self.nome} tentando se inscrever no evento '{evento.nome}'...")
        
        if not evento.validarCapacidade():
            return None

        from ingresso import Ingresso 
        novo_ingresso = Ingresso(id_ingresso, tipo, preco, self, evento)
        
        try:
            evento.adicionarIngresso(novo_ingresso)
        except ValueError as e:
            print(f"Falha ao adicionar ingresso: {e}")
            return None

        self._ingressos.append(novo_ingresso)
        
        print(f"Inscrição de {self.nome} no {evento.nome} bem-sucedida! (Ingresso {novo_ingresso.id})")
        return novo_ingresso

    def cancelarInscricao(self, ingresso: 'Ingresso'):
        if ingresso in self._ingressos:
            print(f"Participante {self.nome} cancelando inscrição (Ingresso {ingresso.id}).")
            ingresso.cancelar()
            self._ingressos.remove(ingresso)
        else:
            print(f"Erro: {self.nome} não possui o ingresso {ingresso.id}.")