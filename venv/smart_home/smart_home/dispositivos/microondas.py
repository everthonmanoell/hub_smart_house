from enum import Enum
from ..core.descriptors import PotenciaWDescriptor
from datetime import datetime
from transitions import Machine

# class PotenciaWDescriptor:
#     def __set_name__(self, owner, name):
#         self.private_name = '_' +name

#     def __get__(self, instance, owner):
#         if instance is None:
#             return self
#         return getattr(instance, self.private_name, None)
    
#     def __set__(self, istance, value):
#         if isinstance(value, int):
#             if value >= 0:
#                 setattr(isinstance, self.private_name, value)
#         raise ValueError(f"O valor: {value} tem que ser >= 0")
    
class EstadosMricoondas(Enum):
    ON = 'on'
    OFF = 'off'
    IN_USE = 'in_use'

class Microondas:
    estados = [e.value for e in EstadosMricoondas]

    transicoes = [
        {'trigger': 'ligar', 'source': EstadosMricoondas.OFF.value, 'dest':EstadosMricoondas.ON.value},
        {'trigger': 'desligar', 'source': EstadosMricoondas.ON.value, 'dest': EstadosMricoondas.OFF.value},
        {'trigger': 'usar', 'source': EstadosMricoondas.ON.value, 'dest': EstadosMricoondas.IN_USE}
    ]
    potencia_w = PotenciaWDescriptor()
    def __init__(self, nome, potencia_w=110, estado_inicial = EstadosMricoondas.OFF):
        self._nome = nome
        self._potencia_w = potencia_w
        self._consumo_wh = 0
        self._hora_ligado = None
        self._estado_inicial = estado_inicial

        self.maquina = Machine(
            model = self,
            states = Microondas.estados,
            initial= estado_inicial
        )
    
    def on_enter_ON(self):
         print(f'Microondas no estado: {self.state} | ligado ')

    def on_enter_IN_USE(self):
        self._hora_ligada = datetime.now()
        print(f'Microondas no estado: {self.state} | Em uso ')

    def on_exit_IN_USE(self):
        diferenca = self._hora_ligada - datetime.now()

        diferenca_em_horas = diferenca.total_seconds() / 3600

        self._consumo_wh = self._potencia_w * diferenca_em_horas
    
    def on_enter_OFF(self):
        print(f'Microondas desligado.')
