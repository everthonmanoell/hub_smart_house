from enum import Enum
from transitions import Machine
from smart_home.core.dispositivos import Dispositivo, TipoDispositivo
from smart_home.core.erros import AtributoInvalidoError


class BrilhoDescriptor: #XXX
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


class CorDescriptor:#XXX
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


class Luz(Dispositivo): #XXX 
    estados = [e.value for e in EstadoLuz]

    transicoes = [#XXX
        {"trigger": "ligar", "source": EstadoLuz.OFF.value, "dest": EstadoLuz.ON.value},
        {"trigger": "desligar", "source": EstadoLuz.ON.value, "dest": EstadoLuz.OFF.value},
        {"trigger": "definir_brilho", "source": EstadoLuz.ON.value, "dest": EstadoLuz.ON.value, "conditions": "validar_brilho"},
        {"trigger": "definir_cor", "source": EstadoLuz.ON.value, "dest": EstadoLuz.ON.value, "conditions": "validar_cor"},
    ]

    brilho = BrilhoDescriptor()
    cor = CorDescriptor()

    def __init__(self, id: str, nome: str, brilho: int = 50, cor: Cor = Cor.NEUTRA, estado_inicial=EstadoLuz.OFF):
        super().__init__(id, nome, TipoDispositivo.LIGHT)
        self.brilho = brilho
        self.cor = cor
        self.maquina = Machine(
            model=self,
            states=Luz.estados,
            transitions=Luz.transicoes,
            initial=estado_inicial.value,
            auto_transitions=False
            
        )


    def get_estado_dict(self) -> dict:
        return {
            "estado": self.state,
            "atributos": {
                "brilho": self.brilho,
                "cor": self.cor.name  # Salvar o nome do Enum (ex: "QUENTE")
            }
        }

    # Validação de brilho
    def validar_brilho(self):
        return 0 <= self._brilho <= 100
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