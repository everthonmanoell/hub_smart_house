
from enum import Enum
from transitions import Machine
from smart_home.core.dispositivos import Dispositivo, TipoDispositivo

class EstadoPorta(Enum):
    ABERTA = "aberta"
    DESTRANCADA = "destrancada"
    TRANCADA = "trancada"

class Porta(Dispositivo):
    
    estados = [e.value for e in EstadoPorta]
    transicoes = [
        {"trigger": "abrir", "source": EstadoPorta.DESTRANCADA.value, "dest": EstadoPorta.ABERTA.value},
        {"trigger": "fechar", "source": EstadoPorta.ABERTA.value, "dest": EstadoPorta.DESTRANCADA.value},
        {"trigger": "trancar", "source": EstadoPorta.DESTRANCADA.value, "dest": EstadoPorta.TRANCADA.value, "conditions": "pode_trancar"},
        {"trigger": "destrancar", "source": EstadoPorta.TRANCADA.value, "dest": EstadoPorta.DESTRANCADA.value},
    ]

    def __init__(self, id: str, nome: str, estado_inicial=EstadoPorta.TRANCADA):
        super().__init__(id, nome, TipoDispositivo.DOOR)
        self.tentativas_invalidas = 0

        self.maquina = Machine(
            model=self,
            states=Porta.estados,
            transitions=Porta.transicoes,
            # Passa o valor em string do estado inicial
            initial=estado_inicial.value,
            auto_transitions=False
            
            
        )
    
    def get_estado_dict(self) -> dict:
        return {
            "estado": self.state,
            "atributos": {
                "tentativas_invalidas": self.tentativas_invalidas
            }
        }

    # Callbacks
    def on_enter_aberta(self): # Nome do callback muda para corresponder ao estado em string
        print(f"Porta '{self.nome}' abriu.")
    def on_enter_destrancada(self):
        print(f"Porta '{self.nome}' destrancou.")
    def on_enter_trancada(self):
        print(f"Porta '{self.nome}' trancou.")

    # Regra/Condição
    def pode_trancar(self):
        # Compara o estado (string) com o valor do Enum
        if self.state == EstadoPorta.ABERTA.value:
            self.tentativas_invalidas += 1
            print("⚠️ Tentativa inválida! Não pode trancar a porta aberta.")
            return False
        return True