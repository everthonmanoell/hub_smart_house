from enum import Enum
from datetime import datetime
from transitions import Machine

# Descriptor para validar potência
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
            raise ValueError(f"O valor: {value} tem que ser um inteiro >= 0")


class EstadosTv(Enum):
    ON = "on"
    OFF = "off"
    IN_USE = "in_use"


class Tv:
    estados = [e for e in EstadosTv]  # usa Enum, não .value

    transicoes = [
        {"trigger": "ligar", "source": EstadosTv.OFF, "dest": EstadosTv.ON},
        {"trigger": "desligar", "source": EstadosTv.ON, "dest": EstadosTv.OFF},
        {"trigger": "usar", "source": EstadosTv.ON, "dest": EstadosTv.IN_USE},
        {"trigger": "parar", "source": EstadosTv.IN_USE, "dest": EstadosTv.ON},
    ]

    potencia_w = PotenciaWDescriptor()

    def __init__(self, nome, potencia_w=110, estado_inicial=EstadosTv.OFF):
        self._nome = nome
        self.potencia_w = potencia_w
        self._consumo_wh = 0
        self._hora_ligada = None

        # Máquina de estados
        self.maquina = Machine(
            model=self,
            states=Tv.estados,
            transitions=Tv.transicoes,
            initial=estado_inicial,
            ignore_invalid_triggers=True,
        )

    # --- PROPRIEDADES ---
    @property
    def nome(self):
        return self._nome

    @property
    def consumo_wh(self):
        return self._consumo_wh

    # --- CALLBACKS ---
    def on_enter_ON(self):
        print(f"📺 Tv '{self._nome}' ligada. Estado: {self.state}")

    def on_enter_IN_USE(self):
        self._hora_ligada = datetime.now()
        print(f"🎬 Tv '{self._nome}' em uso.")

    def on_exit_IN_USE(self):
        diferenca = datetime.now() - self._hora_ligada
        diferenca_em_horas = diferenca.total_seconds() / 3600
        self._consumo_wh += self.potencia_w * diferenca_em_horas
        print(f"🔌 Consumo acumulado: {self._consumo_wh:.4f} Wh")

    def on_enter_OFF(self):
        print(f"🛑 Tv '{self._nome}' desligada.")

if __name__ == "__main__":
    tv = Tv("Sala", potencia_w=150)

    print(tv.state)  # Estado inicial OFF
    tv.ligar()
    print(tv.state)
    tv.usar()
    print(tv.state)
    tv.parar()
    print(tv.state)
    tv.desligar()
    print(tv.state)
    print(f"Consumo total: {tv.consumo_wh:.2f} Wh")
