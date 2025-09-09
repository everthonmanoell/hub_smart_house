from enum import Enum
from transitions import Machine
from datetime import datetime
from time import sleep

# Descriptor para validar potência
class PotenciaWDescriptor:
    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)
    
    def __set__(self, instance, value):
        if isinstance(value, int) and value >= 0:
            setattr(instance, self.private_name, value)
        else:
            raise ValueError(f"O valor: {value} tem que ser um inteiro >= 0")


class EstadoTomada(Enum):
    ON = 'on'
    OFF = 'off'


class Tomada:
    estados = [e.value for e in EstadoTomada]

    transicoes = [
        {'trigger': 'ligar', 'source': EstadoTomada.OFF.value, 'dest': EstadoTomada.ON.value},
        {'trigger': 'desligar', 'source': EstadoTomada.ON.value, 'dest': EstadoTomada.OFF.value}
    ]

    potencia_w = PotenciaWDescriptor()

    def __init__(self, nome, potencia_w, estado_inicial=EstadoTomada.OFF.value):
        self._nome = nome
        self.potencia_w = potencia_w  # usa descriptor
        self._consumo_wh = 0
        self._estado_inicial = estado_inicial
        self._hora_ligada = None

        # Criar máquina de estados
        self.maquina = Machine(
            model=self,
            states=Tomada.estados,
            transitions=Tomada.transicoes,
            initial=estado_inicial
        )

    # --- PROPERTIES ---
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor:
            raise ValueError("O nome da tomada não pode ser vazio.")
        self._nome = valor

    @property
    def consumo_wh(self):
        return self._consumo_wh

    # --- CALLBACKS ---
    def on_enter_ON(self):
        self._hora_ligada = datetime.now()
        print(f"⚡ Tomada '{self._nome}' ligada. Estado: {self.state}")

    def on_exit_ON(self):
        diferenca = datetime.now() - self._hora_ligada
        diferenca_em_horas = diferenca.total_seconds() / 3600
        self._consumo_wh += self.potencia_w * diferenca_em_horas
        print(f"🔌 Consumo acumulado: {self._consumo_wh:.2f} Wh")

    def on_enter_OFF(self):
        print(f"🛑 Tomada '{self._nome}' desligada.")


if __name__ == "__main__":
    tomada = Tomada("Tomada da sala", 110)

    tomada.ligar()       # ⚡ Tomada 'Tomada da sala' ligada. Estado: on
    sleep(2)           # Simula 2 segundos ligada
    tomada.desligar()    # 🛑 Tomada 'Tomada da sala' desligada.
    print(f"Consumo total: {tomada.consumo_wh:.6f} Wh")
