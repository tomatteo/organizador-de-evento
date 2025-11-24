from datetime import datetime

class Relatorio:
    def __init__(self, id: int, conteudo: str):
        self._id = id
        self._dataGeracao = datetime.now()
        self._conteudo = conteudo
    
    @property
    def conteudo(self) -> str: return self._conteudo

    def gerarResumo(self) -> str:
        return (f"Relatório ID {self._id} (Gerado em: {self._dataGeracao.strftime('%Y-%m-%d')})\n"
                + "="*20 + f"\n{self.conteudo}")