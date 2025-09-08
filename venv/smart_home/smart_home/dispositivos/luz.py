from enum import Enum
from transitions import Machine

class EstadoLuz(Enum):
    ON = 'on'
    OFF = 'off'

class Cor(Enum):
    QUENTE = 'quente'
    FRIA = 'fria'
    NEUTRA = 'neutra'


class Luz:
    estados = [e.value for e in EstadoLuz]

    transicoes = [
        {'trigger': 'ligar', 'source': EstadoLuz.OFF.value, 'dest': EstadoLuz.ON.value},
        {'trigger': 'desligar', 'source': EstadoLuz.ON.value, 'dest': EstadoLuz.OFF.value},
        {'trigger': 'definir_brilho', 'source': EstadoLuz.ON, 'dest': EstadoLuz.ON, 'conditions': 'validar_brilho'},
        {'trigger': 'definir_cor', 'source': EstadoLuz.ON, 'dest': EstadoLuz.ON, 'conditions': 'validar_cor'}
        
    ]

    def __init__(self, nome, estado_inicial = EstadoLuz.OFF.value):
        self._nome = nome
        self._brilho = 0
        self._cor = Cor.NEUTRA
        
        self.maquina = Machine(
            model=self,
            states=Luz.estados,
            initial=estado_inicial,      
        )

    # - Brilho e validação
    @property
    def brilho(self):
        return self._brilho
    
    @brilho.setter
    def brilho(self, valor):
        self._brilho = valor

    def validar_brilho(self):
        if self.brilho >= 0 and self.brilho <= 100:
            return True
        return False
    
    # Cor e validacao
    @property
    def cor(self):
        return self._cor
    
    @cor.setter
    def cor(self, valor):
        self._cor = valor

    def validar_cor(self, valor):
        if isinstance(valor, Cor):
            return True
        return False

    
    # Callbacks dos eventos
    def on_enter_on(self):
        print(f"Luz {self.nome} ligada.")

    def on_enter_off(self):
        print(f"Luz {self.nome} desligada.")

    def definir_brilho(self, brilho):
        self.brilho = brilho
        print(f"Brilho ajustado para {self.brilho}.")

    def definir_cor(self, cor: Cor):
        self.cor = cor
        print(f"Cor ajustada para {self.cor.value}.")
    
    