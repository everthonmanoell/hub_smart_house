from enum import Enum
from transitions import Machine
from datetime import datetime
# from smart_home.core.persistencia import salvar_tempo_tomada_json

class PotenciaWDescriptor:
    def __set_name__(self, owner, name):
        self.private_name = '_' +name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)
    
    def __set__(self, istance, value):
        if isinstance(value, int):
            if value >= 0:
                setattr(isinstance, self.private_name, value)
        raise ValueError(f"O valor: {value} tem que ser >= 0")
class EstadoTomada(Enum):
    ON = 'on'
    OFF = 'off' 
class Tomada:
    estados = [e.value for e in EstadoTomada]

    transicoes = [
        {'trigger': 'ligar', 'source' : EstadoTomada.OFF.value, 'dest': EstadoTomada.ON.value},
        {'trigger': 'desligar', 'source': EstadoTomada.ON.value, 'dest': EstadoTomada.OFF.value}
    ]

    potencia_w = PotenciaWDescriptor()
    def __init__(self, nome, potencia_w, estado_inicial = EstadoTomada.OFF.value):
        self._nome = nome
        self._potencia_w = potencia_w
        self._consumo_wh = 0
        self._estado_inicial = estado_inicial
        self._hora_ligada = None

        self.maquina = Machine(
            model = self,
            states=Tomada.estados,
            initial=estado_inicial
        )


    def on_enter_ON(self):
        self._hora_ligada = datetime.now()
        print(f'Tomada no estado: {self.state} | ligado')

    def on_exit_ON(self):
        diferenca = self._hora_ligada - datetime.now()

        diferenca_em_horas = diferenca.total_seconds() / 3600

        self._consumo_wh = self._potencia_w * diferenca_em_horas
    
    def on_enter_OFF(self):
        print(f'Tomada desligada.')
    
if __name__ == "__main__":
    pass

