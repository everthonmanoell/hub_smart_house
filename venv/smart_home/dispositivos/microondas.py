# smart_home/dispositivos/microondas.py

from enum import Enum
from datetime import datetime
from transitions import Machine
from smart_home.core.dispositivos import Dispositivo, TipoDispositivo
from smart_home.core.erros import AtributoInvalidoError

class PotenciaWDescriptor:
    def __set_name__(self, owner, name):
        self.private_name = "_" + name
    def __get__(self, instance, owner):
        return getattr(instance, self.private_name, None)
    def __set__(self, instance, value):
        if isinstance(value, int) and value >= 0:
            setattr(instance, self.private_name, value)
        else:
            # Corrigido para usar a exceção personalizada
            raise AtributoInvalidoError(f"O valor de potência: {value} tem que ser >= 0")

class EstadosMicroondas(Enum):
    ON = "on"
    OFF = "off"
    IN_USE = "in_use"

class Microondas(Dispositivo):
    estados = [e.value for e in EstadosMicroondas]

    transicoes = [
        {"trigger": "ligar", "source": "off", "dest": "on"},
        {"trigger": "desligar", "source": "on", "dest": "off"},
        {"trigger": "usar", "source": "on", "dest": "in_use"},
        {"trigger": "parar", "source": "in_use", "dest": "on"},
    ]

    potencia_w = PotenciaWDescriptor()

    def __init__(self, id: str, nome: str, potencia_w=1100, estado_inicial=EstadosMicroondas.OFF):
        super().__init__(id, nome, TipoDispositivo.MICROWAVE)
        self.potencia_w = potencia_w
        self._consumo_wh = 0
        self._hora_ligada = None
        self.maquina = Machine(
            model=self,
            states=Microondas.estados,
            transitions=Microondas.transicoes,
            initial=estado_inicial.value,
            auto_transitions=False
        )

    def get_estado_dict(self) -> dict:
        return { "estado": self.state, "atributos": { "potencia_w": self.potencia_w } }

    # --- CORREÇÃO 3: Renomear os callbacks para minúsculas ---
    def on_enter_on(self):
        print(f"Microondas '{self.nome}' ligado.")

    def on_enter_in_use(self):
        self._hora_ligada = datetime.now()
        print(f"Microondas '{self.nome}' em uso.")

    def on_exit_in_use(self):
        if self._hora_ligada:
            diferenca = datetime.now() - self._hora_ligada
            diferenca_em_horas = diferenca.total_seconds() / 3600
            self._consumo_wh += self.potencia_w * diferenca_em_horas

    def on_enter_off(self):
        print(f"Microondas '{self.nome}' desligado.")

    @property
    def consumo_wh(self):
        return self._consumo_wh