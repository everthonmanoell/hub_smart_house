from enum import Enum
from transitions import Machine


class BrilhoDescriptor:
    def __set_name__(self, owner, name):
        self.private_name = '_' + name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('O valor deve ser >= 0 e <= 100')
        setattr(instance, self.private_name, value)


class CorDescriptor:
    def __set_name__(self, owner, name):
        self.private_name = '_' + name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)
    
    def __set__(self, instance, value):
        if not isinstance(value, Cor):
            raise ValueError(f'Cor deve ser do tipo {Cor}')
        setattr(instance, self.private_name, value)


class EstadoLuz(Enum):
    ON = "on"
    OFF = "off"


class Cor(Enum):
    QUENTE = "quente"
    FRIA = "fria"
    NEUTRA = "neutra"


class Luz:
    estados = list(EstadoLuz)

    transicoes = [
        {"trigger": "ligar", "source": EstadoLuz.OFF, "dest": EstadoLuz.ON},
        {"trigger": "desligar", "source": EstadoLuz.ON, "dest": EstadoLuz.OFF},
        {"trigger": "definir_brilho", "source": EstadoLuz.ON, "dest": EstadoLuz.ON, "conditions": "validar_brilho"},
        {"trigger": "definir_cor", "source": EstadoLuz.ON, "dest": EstadoLuz.ON, "conditions": "validar_cor"},
    ]

    brilho = BrilhoDescriptor()
    cor = CorDescriptor()

    def __init__(self, nome, brilho, cor=Cor.NEUTRA, estado_inicial=EstadoLuz.OFF):
        self._nome = nome
        self._brilho = brilho
        self._cor = cor

        self.maquina = Machine(
            model=self,
            states=Luz.estados,
            transitions=Luz.transicoes,
            initial=estado_inicial,
        )
    #==== Brilho=======
    @property
    def brilho(self):
        return self._brilho
    
    @brilho.setter
    def brilho(self, brilho):
        self._brilho = brilho
        print(f"Brilho ajustado para {self._brilho}.")

    # Validação de brilho
    def validar_brilho(self):
        return 0 <= self._brilho <= 100

    #==== Cor =======
    @property
    def cor(self):
        return self._cor
    
    @cor.setter
    def cor(self, cor):
        self._cor = cor
        print(f"Cor ajustada para {self._cor.value}.")

    # Validação de cor
    def validar_cor(self):
        return isinstance(self._cor, Cor)

    # Callbacks
    def on_enter_ON(self):
        print(f"Luz {self._nome} ligada.")

    def on_enter_OFF(self):
        print(f"Luz {self._nome} desligada.")

if __name__ == "__main__":
    luz = Luz("Sala", brilho=75, cor=Cor.QUENTE)

    print(luz.state)  # Estado inicial OFF
    luz.ligar()
    print(luz.state)  # Estado ON

    luz.brilho = 85
    luz.definir_brilho()  # Ajusta o brilho

    luz.cor = Cor.FRIA
    luz.definir_cor()  # Ajusta a cor

    luz.desligar()
    print(luz.state)  # Estado OFF