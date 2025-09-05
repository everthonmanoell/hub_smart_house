from enum import Enum, auto

class EstadoPorta(Enum):
    ABERTA = auto()
    FECHADA = auto()
    TRACADA = auto()
    DESTRANCADA = auto()
class Porta:
    def __init__(self):
        self.esta_aberta = False

    def abrir(self):
        if not self.esta_aberta:
            self.esta_aberta = True
            return "Porta aberta."
        return "A porta já está aberta."
    
    def fechar(self):
        if self.esta_aberta:
            self.esta_aberta = False
            return "Porta fechada."
        return "A porta já está fechada."
