from usuario import Usuario
from evento import Evento
from relatorio import Relatorio

class Administrador(Usuario):
    def __init__(self, id: int, nome: str, email: str, senha: str):
        super().__init__(id, nome, email, senha)

    def autenticar(self, senha: str) -> bool:
        is_valid = self._senha == senha
        print(f"Autenticação (Admin) para {self.nome}: {'Sucesso' if is_valid else 'Falha'}")
        return is_valid

    def gerarRelatorios(self, usuarios: list[Usuario], eventos: list[Evento]) -> Relatorio:
        print(f"ADM {self.nome} está gerando relatórios...")
        conteudo = "--- Relatório de Usuários ---\n"
        conteudo += f"Total de usuários: {len(usuarios)}\n"
        for user in usuarios:
            conteudo += f"- {user.nome} ({user.__class__.__name__})\n"
        
        conteudo += "\n--- Relatório de Eventos ---\n"
        conteudo += f"Total de eventos: {len(eventos)}\n"
        for evento in eventos:
            vagas_ocupadas = len([ing for ing in evento.ingressos if ing.status == "Vendido"])
            conteudo += f"- {evento.nome} ({vagas_ocupadas}/{evento.capacidade} ingressos)\n"

    
        from datetime import datetime
        return Relatorio(id=datetime.now().microsecond, conteudo=conteudo)

    def gerenciarUsuarios(self, usuario: Usuario, acao: str):
        print(f"ADM {self.nome} executou a ação '{acao}' no usuário '{usuario.nome}'.")