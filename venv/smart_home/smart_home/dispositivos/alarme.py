from enum import Enum
from transitions import Machine

class EstadosAlarme(Enum):
    ON = 'on'
    OFF = 'off'
    TRIGGERED = 'triggered'


class Alarme:
    estados = [e.value for e in EstadosAlarme]

    transicoes = [
        {'trigger': 'ligar', 'source' : EstadosAlarme.OFF.value, 'dest': EstadosAlarme.ON.value},
        {'trigger': 'desligar', 'source': EstadosAlarme.ON.value, 'dest': EstadosAlarme.OFF.value},
        {'trigger': 'alarmar', 'source': EstadosAlarme.ON.value, 'dest': EstadosAlarme.TRIGGERED.value},
        {'trigger': 'desativar_alarmar', 'source': EstadosAlarme.TRIGGERED.value, 'dest':EstadosAlarme.ON.value }
    ]

    def __init__(self, nome, estado_inicial = EstadosAlarme.OFF.value):
        self._nome = nome
        self._estado_inicial = estado_inicial

        self.maquina = Machine(
            model = self,
            states= Alarme.estados,
            initial=estado_inicial
        )

    