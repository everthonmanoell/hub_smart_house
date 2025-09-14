from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any

class TipoEvento(Enum):
    COMANDO_EXECUTADO = "ComandoExecutado"
    DISPOSITIVO_ADICIONADO = "DispositivoAdicionado"
    DISPOSITIVO_REMOVIDO = "DispositivoRemovido"

class Evento:
    def __init__(self, tipo: TipoEvento, id_dispositivo: str, detalhes: Optional[Dict[str, Any]] = None, **kwargs):
        self.timestamp = datetime.now().isoformat()
        self.tipo = tipo
        self.id_dispositivo = id_dispositivo
        self.dados = detalhes or {}
        self.dados.update(kwargs) 

    def __str__(self):
        if self.tipo == TipoEvento.DISPOSITIVO_ADICIONADO:
            return f"[EVENTO] {self.tipo.value}: {{'id': '{self.id_dispositivo}', 'tipo': '{self.dados.get('tipo_dispositivo')}'}}"
        
        elif self.tipo == TipoEvento.DISPOSITIVO_REMOVIDO:
            return f"[EVENTO] {self.tipo.value}: {{'id': '{self.id_dispositivo}', 'tipo': '{self.dados.get('tipo_dispositivo')}'}}"
            
        elif self.tipo == TipoEvento.COMANDO_EXECUTADO:
            d = self.dados
            return f"[EVENTO] {self.tipo.value}: {{'id': '{self.id_dispositivo}', 'comando': '{d.get('comando')}', 'antes': '{d.get('estado_antes')}', 'depois': '{d.get('estado_depois')}'}}"
            
        # Formato padrão para outros eventos
        return f"[{self.tipo.value}] {self.id_dispositivo}: {self.dados}"