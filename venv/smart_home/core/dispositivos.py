
from abc import ABC, abstractmethod
from enum import Enum

class TipoDispositivo(Enum):
    DOOR = "PORTA"
    LIGHT = "LUZ"
    OUTLET = "TOMADA"
    ALARM = "ALARME"
    MICROWAVE = "MICROONDAS"
    TV = "TV"

class Dispositivo(ABC):
    def __init__(self, id: str, nome: str, tipo: TipoDispositivo):
        self._id = id
        self._nome = nome
        self._tipo = tipo

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def tipo(self):
        return self._tipo
    

    @abstractmethod
    def get_estado_dict(self) -> dict:
        pass

    def __str__(self):
        # self.state vai acessar diretamente o atributo criado pela FSM
        return f"{self.id} | {self.tipo.value} | {self.state}"