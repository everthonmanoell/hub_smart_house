from enum import Enum, auto

class Bebida(Enum):
    EXPRESSO = auto()
    CAPPUCINO = auto()
    LATTE = auto()

NOMES = {
    'espresso' : Bebida.EXPRESSO,
    'latte' : Bebida.LATTE,
    'cappuccino' : Bebida.CAPPUCINO
}
class Cafeteria:
    def __init__(self, on = False):
        self.bebida_selecionada = None
        self.credito = 0

    def inserir(self, valor = 1):
        self.credito += valor

    