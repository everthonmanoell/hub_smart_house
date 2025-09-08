from enum import Enum
from transitions import Machine
from datetime import datetime, time

class PotenciaWDescriptor:
    def __set_name__(self, owner, name):
        self.private_name = '_' +name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)
    
    def __set__(self, istance, value):
        if isinstance(value, int):
            if value >= 0:
                setattr(isinstance, self.private_name, value)
        raise ValueError(f"O valor: {value} tem que ser >= 0")
class EstadoTomada(Enum):
    ON = 'on'
    OFF = 'off' 
class Tomada:
    estados = [e.value for e in EstadoTomada]

    transicoes = [{'trigger': 'ligar', 'source' : EstadoTomada.OFF.value, 'dest': EstadoTomada.ON.value},
                   {'trigger': 'desligar', 'source': EstadoTomada.ON.value, 'dest': EstadoTomada.OFF.value}
    ]

    potencia_w = PotenciaWDescriptor()
    def __init__(self, nome, potencia_w):
        self.nome = nome
        self.potencia_w = potencia_w
        
