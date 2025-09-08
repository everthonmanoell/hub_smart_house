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
    
class EstadosTv(Enum):
    ON = 'on'
    OFF = 'off'
    IN_USE = 'in_use'

class Tv:
    estados = [e.value for e in EstadosTv]

    transicoes = [
        {'trigger': 'ligar', 'source': EstadosTv.OFF.value, 'dest':EstadosTv.ON.value},
        {'trigger': 'desligar', 'source': EstadosTv.ON.value, 'dest': EstadosTv.OFF.value},
        {'trigger': 'usar', 'source': EstadosTv.ON.value, 'dest': EstadosTv.IN_USE}
    ]
    potencia_w = PotenciaWDescriptor()
    def __init__(self, nome, potencia_w=110, estado_inicial = EstadosTv.OFF):
        self._nome = nome
        self._potencia_w = potencia_w
        self._consumo_wh = 0
        self._hora_ligado = None
        self._estado_inicial = estado_inicial

        self.maquina = Machine(
            model = self,
            states = Tv.estados,
            initial= estado_inicial
        )
    
    def on_enter_ON(self):
         print(f'Tv no estado: {self.state} | ligado ')

    def on_enter_IN_USE(self):
        self._hora_ligada = datetime.now()
        print(f'Tv no estado: {self.state} | Em uso ')

    def on_exit_IN_USE(self):
        diferenca = self._hora_ligada - datetime.now()

        diferenca_em_horas = diferenca.total_seconds() / 3600

        self._consumo_wh = self._potencia_w * diferenca_em_horas
    
    def on_enter_OFF(self):
        print(f'Tv desligado.')
