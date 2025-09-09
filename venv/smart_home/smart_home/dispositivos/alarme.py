from enum import Enum
from transitions import Machine

class EstadosAlarme(Enum):
    ON = 'on'
    OFF = 'off'
    TRIGGERED = 'triggered'


class Alarme:
    estados = list(EstadosAlarme)

    transicoes = [
        {'trigger': 'ligar', 'source' : EstadosAlarme.OFF, 'dest': EstadosAlarme.ON},
        {'trigger': 'desligar', 'source': EstadosAlarme.ON, 'dest': EstadosAlarme.OFF},
        {'trigger': 'alarmar', 'source': EstadosAlarme.ON, 'dest': EstadosAlarme.TRIGGERED},
        {'trigger': 'desativar_alarme', 'source': EstadosAlarme.TRIGGERED, 'dest':EstadosAlarme.ON }
    ]

    def __init__(self, nome, estado_inicial = EstadosAlarme.OFF):
        self._nome = nome
        self._estado_inicial = estado_inicial

        self.maquina = Machine(
            model = self,
            states= Alarme.estados,
            transitions= Alarme.transicoes,
            initial=estado_inicial
        )

    def on_enter_ON(self):
        print(f"Alarme {self._nome} ligado.")
    
    def on_enter_OFF(self):
        print(f"Alarme {self._nome} desligado.")
    
    def on_enter_TRIGGERED(self):
        print(f"🚨 Alarme {self._nome} disparado! 🚨")
    
    # # Machine
    # @property
    # def maquina(self):
    #     return self._maquina
    
    @property
    def nome(self):
        return self._nome
    @nome.setter
    def nome(self, nome):
        self._nome = nome
    
if __name__ == "__main__":
    alarme = Alarme("Casa")

    print(alarme.state)
    alarme.ligar()
    print(alarme.state)        # "Alarme Casa ligado."
    alarme.alarmar()
    print(alarme.state)      # "🚨 Alarme Casa disparado!
    alarme.desativar_alarme()
    print(alarme.state)  # "Alarme Casa ligado."
    alarme.desligar()
    print(alarme.state)      # "Alarme Casa desligado."

