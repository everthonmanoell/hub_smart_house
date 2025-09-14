# smart_home/core/logger.py
import csv
import os
from threading import Lock
from .observers import Observer
from .eventos import Evento, TipoEvento

class CSVLogger(Observer):
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, filepath='smart_home/data/eventos.csv'):
        if not hasattr(self, 'initialized'):
            self.filepath = filepath
            self.initialized = True

    def update(self, evento: Evento):
        if evento.tipo == TipoEvento.COMANDO_EXECUTADO and evento.dados.get('estado_antes') != evento.dados.get('estado_depois'):
            self.log_event(evento)

    def log_event(self, evento: Evento):
        with self._lock:
            try:
                os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
                escrever_cabecalho = not os.path.exists(self.filepath) or os.path.getsize(self.filepath) == 0
                with open(self.filepath, 'a', newline='', encoding='utf-8') as f:
                    header = ['timestamp', 'id_dispositivo', 'evento', 'estado_origem', 'estado_destino']
                    writer = csv.DictWriter(f, fieldnames=header, extrasaction='ignore')
                    if escrever_cabecalho:
                        writer.writeheader()
                    linha = {
                        'timestamp': evento.timestamp,
                        'id_dispositivo': evento.id_dispositivo,
                        'evento': evento.dados.get('comando', 'N/A'),
                        'estado_origem': evento.dados.get('estado_antes', 'N/A'),
                        'estado_destino': evento.dados.get('estado_depois', 'N/A'),
                    }
                    writer.writerow(linha)
            except Exception as e:
                print(f"[ERRO NO LOGGER]: Não foi possível escrever no arquivo de log: {e}")

    def close(self):
        pass