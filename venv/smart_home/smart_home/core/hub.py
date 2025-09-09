from smart_home.core.observers import ConsoleObserver, ArquivoObserver
import json

class HubAutomacao:
    def __init__(self):
        self.dispositivos = {}
        self.observers = []
        self.rotinas = {}

    # Dispositivos
    def adicionar_dispositivo(self, dispositivo):
        self.dispositivos[dispositivo.nome] = dispositivo
        self.notificar_observers(f"Dispositivo {dispositivo.nome} adicionado ao Hub.")

    def listar_dispositivos(self):
        return list(self.dispositivos.keys())
    
    def remover_dispositivo(self, nome):
        if nome in self.dispositivos:
            del self.dispositivos[nome]
            self.notificar_observers(f"Dispositivo {nome} removido do Hub.")
        else:
            print(f"Dispositivo {nome} não encontrado.")

    # Observers
    def adicionar_observer(self, observer):
        self.observers.append(observer)
    
    def notificar_observers(self, mensagem):
        for observer in self.observers:
            observer.update(mensagem)
    