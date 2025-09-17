from enum import Enum
from transitions import Machine
from smart_home.core.dispositivos import Dispositivo, TipoDispositivo

class EstadosAlarme(Enum):
    ON = 'on'
    OFF = 'off'
    TRIGGERED = 'triggered'


class Alarme(Dispositivo):
    estados = [e.value for e in EstadosAlarme]

    transicoes = [
        {'trigger': 'ligar', 'source' : EstadosAlarme.OFF.value, 'dest': EstadosAlarme.ON.value},
        {'trigger': 'desligar', 'source': EstadosAlarme.ON.value, 'dest': EstadosAlarme.OFF.value},
        {'trigger': 'alarmar', 'source': EstadosAlarme.ON.value, 'dest': EstadosAlarme.TRIGGERED.value},
        {'trigger': 'desativar_alarme', 'source': EstadosAlarme.TRIGGERED.value, 'dest':EstadosAlarme.ON.value }
    ]

    def __init__(self, id: str, nome:str , estado_inicial = EstadosAlarme.OFF):
        super().__init__(id, nome, TipoDispositivo.ALARM)
        self._estado_inicial = estado_inicial

        self.maquina = Machine(
            model = self,
            states= Alarme.estados,
            transitions= Alarme.transicoes,
            initial=estado_inicial.value,
            auto_transitions=False
            
        )
    def get_estado_dict(self) -> dict:
        return {
            "estado": self.state,
            "atributos": {}  # Alarme não tem atributos extras para salvar
        }

    def on_enter_ON(self):
        print(f"Alarme {self._nome} ligado.")
    
    def on_enter_OFF(self):
        print(f"Alarme {self._nome} desligado.")
    
    def on_enter_TRIGGERED(self):
        print(f"🚨 Alarme {self._nome} disparado! 🚨")
    
    
if __name__ == "__main__":
    alarme = Alarme("Casa")

    print(alarme.state)
    alarme.ligar()
    print(alarme.state)        # "Alarme Casa ligado."
    alarme.alarmar()
    print(alarme.state)      # "🚨 Alarme Casa disparado!
    alarme.desativar_alarme()
    print(alarme.state)  # "Alarme Casa ligado."
    alarme.desligar()
    print(alarme.state)      # "Alarme Casa desligado."

