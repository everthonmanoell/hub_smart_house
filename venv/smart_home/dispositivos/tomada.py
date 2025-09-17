from enum import Enum
from transitions import Machine
from datetime import datetime
from time import sleep
from smart_home.core.dispositivos import Dispositivo, TipoDispositivo

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


class Tomada(Dispositivo):
    estados = [e.value for e in EstadoTomada]

    transicoes = [
        {'trigger': 'ligar', 'source': EstadoTomada.OFF.value, 'dest': EstadoTomada.ON.value},
        {'trigger': 'desligar', 'source': EstadoTomada.ON.value, 'dest': EstadoTomada.OFF.value}
    ]

    potencia_w = PotenciaWDescriptor()

    def __init__(self, id: str, nome: str, potencia_w: int, estado_inicial=EstadoTomada.OFF):
        super().__init__(id, nome, TipoDispositivo.OUTLET)
        self.potencia_w = potencia_w
        self._consumo_wh = 0
        self._hora_ligada = None
        self.maquina = Machine(
            model=self,
            states=Tomada.estados,
            transitions=Tomada.transicoes,
            initial=estado_inicial.value,
            auto_transitions=False
            
        )

    def get_estado_dict(self) -> dict:
        return {
            "estado": self.state,
            "atributos": {
                "potencia_w": self.potencia_w,
                "consumo_wh": self._consumo_wh # Salva o consumo atual
            }
        }

    # --- PROPERTIES ---

    @property
    def consumo_wh(self):
        return self._consumo_wh

    # --- CALLBACKS ---
    def on_enter_ON(self):
        self._hora_ligada = datetime.now()
        print(f"⚡ Tomada '{self.nome}' ligada.")
    def on_exit_ON(self):
        if self._hora_ligada:
            diferenca = datetime.now() - self._hora_ligada
            diferenca_em_horas = diferenca.total_seconds() / 3600
            self._consumo_wh += self.potencia_w * diferenca_em_horas
    def on_enter_OFF(self):
        print(f"🛑 Tomada '{self._nome}' desligada.")


if __name__ == "__main__":
    tomada = Tomada("Tomada da sala", 110)

    tomada.ligar()       # ⚡ Tomada 'Tomada da sala' ligada. Estado: on
    sleep(2)           # Simula 2 segundos ligada
    tomada.desligar()    # 🛑 Tomada 'Tomada da sala' desligada.
    print(f"Consumo total: {tomada.consumo_wh:.6f} Wh")
