# smart_home/core/observers.py
from abc import ABC, abstractmethod
from .eventos import Evento

class Observer(ABC):
    @abstractmethod
    def update(self, evento: Evento):
        pass

class ConsoleObserver(Observer):
    def update(self, evento: Evento):
        print(f"[EVENTO CONSOLE] {evento}")

