
from typing import Dict, List
from .dispositivos import Dispositivo
from .persistencia import carregar_de_json, salvar_em_json
from .erros import DispositivoNaoEncontradoError, ComandoInvalidoError, ConfiguracaoInvalidaError
from .eventos import Evento, TipoEvento
from .observers import Observer
from .dispositivos import TipoDispositivo
from smart_home.dispositivos.porta import Porta
from smart_home.dispositivos.luz import Luz, Cor
from smart_home.dispositivos.tomada import Tomada
from smart_home.dispositivos.alarme import Alarme
from smart_home.dispositivos.microondas import Microondas
from smart_home.dispositivos.tv import Tv

TIPO_CLASSE_MAP = {
    TipoDispositivo.DOOR: Porta,
    TipoDispositivo.LIGHT: Luz,
    TipoDispositivo.OUTLET: Tomada,
    TipoDispositivo.ALARM: Alarme,
    TipoDispositivo.MICROWAVE: Microondas,
    TipoDispositivo.TV: Tv,
}

class HubAutomacao:
    def __init__(self, config_path: str):
        self._dispositivos: Dict[str, Dispositivo] = {}
        self._rotinas: Dict[str, List[Dict]] = {}
        self._observers: List[Observer] = []
        self._config_path = config_path
        self.carregar_configuracao()

    def adicionar_observer(self, observer: Observer):
        self._observers.append(observer)

    def _notificar(self, evento: Evento): #XXX
        for observer in self._observers:
            observer.update(evento)

    def adicionar_dispositivo(self, dispositivo: Dispositivo):
        if dispositivo.id in self._dispositivos:
            raise ValueError(f"Dispositivo com ID '{dispositivo.id}' já existe.")
        self._dispositivos[dispositivo.id] = dispositivo
        evento = Evento(TipoEvento.DISPOSITIVO_ADICIONADO, id_dispositivo=dispositivo.id, tipo_dispositivo=dispositivo.tipo.value)
        self._notificar(evento)
        print(f"dispositivo {dispositivo.id} adicionado.")

    def remover_dispositivo(self, id_dispositivo: str):
        if id_dispositivo in self._dispositivos:
            dispositivo = self._dispositivos.pop(id_dispositivo)
            evento = Evento(TipoEvento.DISPOSITIVO_REMOVIDO, id_dispositivo=id_dispositivo, tipo_dispositivo=dispositivo.tipo.value)
            self._notificar(evento)
            print("dispositivo removido")
        else:
            raise DispositivoNaoEncontradoError(f"Dispositivo com ID '{id_dispositivo}' não encontrado.")

    def get_dispositivo(self, id_dispositivo: str) -> Dispositivo:
        dispositivo = self._dispositivos.get(id_dispositivo)
        if not dispositivo:
            raise DispositivoNaoEncontradoError(f"Dispositivo com ID '{id_dispositivo}' não encontrado.")
        return dispositivo

    def listar_dispositivos(self) -> List[Dispositivo]:
        return list(self._dispositivos.values())
        
    def listar_rotinas(self) -> list[str]:
        return list(self._rotinas.keys())

    def executar_comando(self, id_dispositivo: str, comando: str, args: dict = None):
        dispositivo = self.get_dispositivo(id_dispositivo)

        if not hasattr(dispositivo, comando):
            raise ComandoInvalidoError(f"O dispositivo '{id_dispositivo}' não suporta o comando '{comando}'.")

        metodo_verificacao = f"may_{comando}"
        if hasattr(dispositivo, metodo_verificacao) and not getattr(dispositivo, metodo_verificacao)():
            print(f"INFO: Comando '{comando}' não é uma transição válida do estado '{dispositivo.state}'. Comando ignorado.")
            return

        estado_antes = str(dispositivo.state)
        metodo = getattr(dispositivo, comando)

        if args:
            metodo(**args)
        else:
            metodo()
            
        estado_depois = str(dispositivo.state)

        if estado_antes != estado_depois:
            evento = Evento(
                TipoEvento.COMANDO_EXECUTADO, id_dispositivo=id_dispositivo,
                detalhes={"comando": comando, "args": args, "estado_antes": estado_antes, "estado_depois": estado_depois}
            )
            self._notificar(evento)
            print(f"Comando '{comando}' executado em '{id_dispositivo}'. Estado: {estado_antes} -> {estado_depois}")
        elif comando.startswith("definir"):
            print(f"Comando '{comando}' executado em '{id_dispositivo}'. Atributo alterado.")

    def executar_rotina(self, nome_rotina: str):
        print(f"--- Executando rotina: {nome_rotina} ---")
        comandos = self._rotinas[nome_rotina]
        for acao in comandos:
            try:
                self.executar_comando(
                    id_dispositivo=acao["id"],
                    comando=acao["comando"],
                    args=acao.get("argumentos")
                )
            except (DispositivoNaoEncontradoError, ComandoInvalidoError) as e:
                print(f"Erro ao executar ação da rotina: {e}")
        print(f"--- Fim da rotina: {nome_rotina} ---")

    def carregar_configuracao(self):
        try:
            config = carregar_de_json(self._config_path)
        except FileNotFoundError:
            print(f"Arquivo de configuração '{self._config_path}' não encontrado. Iniciando Hub vazio.")
            return

        for dev_data in config.get("dispositivos", []):
            try:
                tipo_enum = TipoDispositivo[dev_data["tipo"]]
                classe_dispositivo = TIPO_CLASSE_MAP[tipo_enum]
                
                args = {"id": dev_data["id"], "nome": dev_data["nome"]}
                if tipo_enum == TipoDispositivo.LIGHT:
                    cor_str = dev_data["atributos"].get("cor", "NEUTRA")
                    args["cor"] = Cor[cor_str]
                    args["brilho"] = dev_data["atributos"].get("brilho", 50)
                elif tipo_enum in (TipoDispositivo.OUTLET, TipoDispositivo.TV, TipoDispositivo.MICROWAVE):
                    args["potencia_w"] = dev_data["atributos"].get("potencia_w", 100)

                dispositivo = classe_dispositivo(**args)
                dispositivo.state = dev_data["estado"]
                self._dispositivos[dispositivo.id] = dispositivo
            except (KeyError, TypeError) as e:
                raise ConfiguracaoInvalidaError(f"Erro ao carregar dispositivo do JSON: {dev_data}. Erro: {e}")

        self._rotinas = config.get("rotinas", {})
        print(f"Configuração carregada de '{self._config_path}'. {len(self._dispositivos)} dispositivos e {len(self._rotinas)} rotinas.")

    def salvar_configuracao(self):
        config = {
            "hub": {"nome": "Casa Exemplo", "versao": "1.0"},
            "dispositivos": [],
            "rotinas": self._rotinas
        }
        for dispositivo in self._dispositivos.values():
            estado_info = dispositivo.get_estado_dict()
            config["dispositivos"].append({
                "id": dispositivo.id, "tipo": dispositivo.tipo.name, "nome": dispositivo.nome, **estado_info
            })
        salvar_em_json(self._config_path, config)
        print("configuracao salva.")