from enum import Enum
from datetime import datetime
from transitions import Machine


class PotenciaWDescriptor:
    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance, value):
        if isinstance(value, int) and value >= 0:
            setattr(instance, self.private_name, value)
        else:
            raise ValueError(f"O valor: {value} tem que ser >= 0")


class EstadosMicroondas(Enum):
    ON = "on"
    OFF = "off"
    IN_USE = "in_use"


class Microondas:
    estados = list(EstadosMicroondas)

    transicoes = [
        {"trigger": "ligar", "source": EstadosMicroondas.OFF, "dest": EstadosMicroondas.ON},
        {"trigger": "desligar", "source": EstadosMicroondas.ON, "dest": EstadosMicroondas.OFF},
        {"trigger": "usar", "source": EstadosMicroondas.ON, "dest": EstadosMicroondas.IN_USE},
        {"trigger": "parar", "source": EstadosMicroondas.IN_USE, "dest": EstadosMicroondas.ON},
    ]

    potencia_w = PotenciaWDescriptor()
    def __init__(self, nome, potencia_w=110, estado_inicial=EstadosMicroondas.OFF):
        self._nome = nome
        self.potencia_w = potencia_w  # usa o descriptor corretamente
        self._consumo_wh = 0
        self._hora_ligada = None

        self.fsm = Machine(
            model=self,
            states=Microondas.estados,
            transitions=Microondas.transicoes,
            initial=estado_inicial,
        )

    def on_enter_ON(self):
        print(f"Microondas no estado: {self.state} | ligado")

    def on_enter_IN_USE(self):
        self._hora_ligada = datetime.now()
        print(f"Microondas no estado: {self.state} | Em uso")

    def on_exit_IN_USE(self):
        diferenca = datetime.now() - self._hora_ligada
        diferenca_em_horas = diferenca.total_seconds() / 3600
        self._consumo_wh += self.potencia_w * diferenca_em_horas
        print(f"Consumo acumulado: {self._consumo_wh:.2f} Wh")

    def on_enter_OFF(self):
        print("Microondas desligado.")

    @property
    def consumo_wh(self):
        return self._consumo_wh

    @property
    def nome(self):
        return self._nome


if __name__ == "__main__":
    microondas = Microondas("Microondas da Cozinha")

    print(microondas.state)
    microondas.ligar()
    print(microondas.state)
    microondas.usar()
    print(microondas.state)
    microondas.parar()
    print(microondas.state)
    microondas.desligar()
    print(microondas.state)
    print(f"Consumo total: {microondas.consumo_wh:.2f} Wh")
