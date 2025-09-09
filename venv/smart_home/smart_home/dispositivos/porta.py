from enum import Enum
from transitions import Machine


class EstadoPorta(Enum):
    ABERTA = "aberta"
    DESTRANCADA = "destrancada"
    TRANCADA = "trancada"


class Porta:
    # agora usamos diretamente os Enums
    estados = list(EstadoPorta)

    transicoes = [
        {"trigger": "abrir", "source": EstadoPorta.DESTRANCADA, "dest": EstadoPorta.ABERTA},
        {"trigger": "fechar", "source": EstadoPorta.ABERTA, "dest": EstadoPorta.DESTRANCADA},
        {"trigger": "trancar", "source": EstadoPorta.DESTRANCADA, "dest": EstadoPorta.TRANCADA, "conditions": "pode_trancar"},
        {"trigger": "destrancar", "source": EstadoPorta.TRANCADA, "dest": EstadoPorta.DESTRANCADA},
    ]

    def __init__(self, nome, estado_inicial=EstadoPorta.DESTRANCADA):
        self.nome = nome
        self.tentativas_invalidas = 0

        # Criar máquina de estados
        self.maquina = Machine(
            model=self,
            states=Porta.estados,
            transitions=Porta.transicoes,
            initial=estado_inicial,
            on_exception='pode_trancar'
        )

    # Callbacks
    def on_enter_ABERTA(self):
        print("A porta abriu.")

    def on_enter_DESTRANCADA(self):
        print("A porta destrancou.")

    def on_enter_TRANCADA(self):
        print("A porta trancou.")

    # Regras extras
    def pode_trancar(self):
        if self.state == EstadoPorta.ABERTA:
            self.tentativas_invalidas += 1
            print("⚠️ Tentativa inválida! Não pode trancar a porta aberta, precisa estar destrancada.")
            return False
        return True


# Exemplo de uso
if __name__ == "__main__":
    porta = Porta("Entrada")

    porta.abrir()      # "A porta abriu."
    porta.trancar()    # "⚠️ Tentativa inválida! Não pode trancar a porta aberta."
    porta.trancar()
    print(porta.tentativas_invalidas)  # 1
    porta.fechar()     # "A porta destrancou."
    porta.trancar()    # "A porta trancou."
