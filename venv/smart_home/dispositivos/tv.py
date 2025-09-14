# smart_home/dispositivos/tv.py

from enum import Enum
from datetime import datetime
from transitions import Machine
from smart_home.core.dispositivos import Dispositivo, TipoDispositivo
from smart_home.core.erros import AtributoInvalidoError

# Descriptor permanece o mesmo...
class PotenciaWDescriptor:
    def __set_name__(self, owner, name):
        self.private_name = "_" + name
    def __get__(self, instance, owner):
        return getattr(instance, self.private_name)
    def __set__(self, instance, value):
        if isinstance(value, int) and value >= 0:
            setattr(instance, self.private_name, value)
        else:
            raise AtributoInvalidoError(f"Potência '{value}' tem que ser um inteiro >= 0")

class EstadosTv(Enum):
    ON = "on"
    OFF = "off"
    IN_USE = "in_use"

class Tv(Dispositivo): # <-- HERDADO DE DISPOSITIVO
    estados = [e.value for e in EstadosTv]
    transicoes = [
        {"trigger": "ligar", "source": EstadosTv.OFF.value, "dest": EstadosTv.ON.value},
        {"trigger": "desligar", "source": EstadosTv.ON.value, "dest": EstadosTv.OFF.value},
        {"trigger": "usar", "source": EstadosTv.ON.value, "dest": EstadosTv.IN_USE.value},
        {"trigger": "parar", "source": EstadosTv.IN_USE.value, "dest": EstadosTv.ON.value},
    ]
    potencia_w = PotenciaWDescriptor()

    def __init__(self, id: str, nome: str, potencia_w=110, estado_inicial=EstadosTv.OFF):
        super().__init__(id, nome, TipoDispositivo.TV)
        self.potencia_w = potencia_w
        self._consumo_wh = 0
        self._hora_ligada = None
        self.maquina = Machine(
            model=self,
            states=Tv.estados,
            transitions=Tv.transicoes,
            initial=estado_inicial,
            auto_transitions=False
            
        )

    def get_estado_dict(self) -> dict:
        return {
            "estado": self.state,
            "atributos": {
                "potencia_w": self.potencia_w
            }
        }
        
    @property
    def consumo_wh(self):
        return self._consumo_wh
        
    # Callbacks permanecem os mesmos...
    def on_enter_ON(self):
        print(f"📺 TV '{self.nome}' ligada.")
    def on_enter_IN_USE(self):
        self._hora_ligada = datetime.now()
        print(f"🎬 TV '{self.nome}' em uso.")
    def on_exit_IN_USE(self):
        if self._hora_ligada:
            diferenca = datetime.now() - self._hora_ligada
            diferenca_em_horas = diferenca.total_seconds() / 3600
            self._consumo_wh += self.potencia_w * diferenca_em_horas
    def on_enter_OFF(self):
        print(f"🛑 TV '{self.nome}' desligada.")