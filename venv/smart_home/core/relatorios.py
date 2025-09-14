import csv
from datetime import datetime
from functools import reduce
from itertools import groupby
from collections import Counter, defaultdict
from typing import List, Dict, Any

# Importa as classes de dispositivo para checagem de tipo e acesso a atributos
from smart_home.dispositivos.luz import Luz
from smart_home.dispositivos.tomada import Tomada
from smart_home.dispositivos.porta import Porta

# --- FUNÇÃO AUXILIAR PARA CARREGAR DADOS ---

def carregar_eventos(filepath='smart_home/data/eventos.csv') -> List[Dict[str, Any]]:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            eventos = list(reader)
            for evento in eventos:
                evento['timestamp'] = datetime.fromisoformat(evento['timestamp'])
            return eventos
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"ERRO: Falha ao carregar ou processar eventos de '{filepath}': {e}")
        return []

def relatorio_tempo_luz_ligada(eventos: List[Dict[str, Any]], dispositivos: List[Any]) -> Dict[str, float]:
    luzes = filter(lambda d: isinstance(d, Luz), dispositivos)
    report = {}
    for luz in luzes:
        eventos_luz = sorted(
            [e for e in eventos if e['id_dispositivo'] == luz.id],
            key=lambda e: e['timestamp']
        )
        tempo_total_ligada = 0.0
        timestamp_ligou = None
        for evento in eventos_luz:
            if evento['evento'] == 'ligar' and timestamp_ligou is None:
                timestamp_ligou = evento['timestamp']
            elif evento['evento'] == 'desligar' and timestamp_ligou is not None:
                duracao = (evento['timestamp'] - timestamp_ligou).total_seconds()
                tempo_total_ligada += duracao
                timestamp_ligou = None
        report[luz.id] = round(tempo_total_ligada, 2)
    return report

def relatorio_consumo_tomada(eventos: List[Dict[str, Any]], dispositivos: List[Any]) -> Dict[str, float]:
    """
    Calcula o consumo total (em Wh) para cada tomada inteligente.
    Usa FILTER para eventos, MAP para calcular consumos parciais e REDUCE para somar.
    """
    tomadas = filter(lambda d: isinstance(d, Tomada), dispositivos)
    
    report = {}
    for tomada in tomadas:
        potencia_w = tomada.potencia_w
        eventos_tomada = sorted(
            [e for e in eventos if e['id_dispositivo'] == tomada.id],
            key=lambda e: e['timestamp']
        )
        
        consumos_parciais = []
        timestamp_ligou = None

        for evento in eventos_tomada:
            if evento['evento'] == 'ligar' and timestamp_ligou is None:
                timestamp_ligou = evento['timestamp']
            elif evento['evento'] == 'desligar' and timestamp_ligou is not None:
                duracao_s = (evento['timestamp'] - timestamp_ligou).total_seconds()
                duracao_h = duracao_s / 3600
                consumo = potencia_w * duracao_h
                consumos_parciais.append(consumo)
                timestamp_ligou = None
        
        # 1. USA MAP (implícito na list comprehension acima) para criar a lista de consumos
        # 2. USA REDUCE para somar todos os consumos parciais e obter o total
        consumo_total = reduce(lambda acumulador, valor: acumulador + valor, consumos_parciais, 0)
        report[tomada.id] = round(consumo_total, 4)
        
    return report

def relatorio_dispositivos_mais_usados(eventos: List[Dict[str, Any]]) -> List[tuple[str, int]]:
    """
    Ordena os dispositivos pelo número de eventos registrados.
    Usa uma COMPREHENSION para extrair os IDs e SORTED com lambda para ordenar.
    """
    if not eventos:
        return []
    
    # 1. USA GENERATOR EXPRESSION (uma forma de comprehension) para contar
    contagem = Counter(e['id_dispositivo'] for e in eventos)
    
    # 2. USA SORTED com uma função lambda como chave para ordenar os itens do mais para o menos usado
    dispositivos_ordenados = sorted(contagem.items(), key=lambda item: item[1], reverse=True)
    
    return dispositivos_ordenados

# --- RELATÓRIOS ADICIONAIS ---

def relatorio_distribuicao_comandos_por_tipo(eventos: List[Dict[str, Any]], dispositivos: List[Any]) -> Dict[str, Dict[str, int]]:
    """
    Mostra a distribuição de comandos (ligar, desligar) por TIPO de dispositivo.
    Usa GROUPBY para agrupar por tipo e COMPREHENSION para contar.
    """
    # Mapeia ID para tipo para evitar buscas repetidas
    id_para_tipo = {d.id: d.tipo.value for d in dispositivos}
    
    # Adiciona o tipo a cada evento para facilitar o agrupamento
    for evento in eventos:
        evento['tipo_dispositivo'] = id_para_tipo.get(evento['id_dispositivo'], 'DESCONHECIDO')

    # Ordena por tipo para que groupby funcione corretamente
    eventos_ordenados = sorted(eventos, key=lambda e: e['tipo_dispositivo'])
    
    report = defaultdict(Counter)
    # 1. USA GROUPBY para agrupar todos os eventos por tipo de dispositivo
    for tipo, eventos_do_tipo in groupby(eventos_ordenados, key=lambda e: e['tipo_dispositivo']):
        # 2. USA COUNTER com GENERATOR EXPRESSION para contar os comandos dentro de cada grupo
        contador_comandos = Counter(e['evento'] for e in eventos_do_tipo)
        report[tipo] = dict(contador_comandos)
        
    return dict(report)

def relatorio_tentativas_invalidas_porta(dispositivos: List[Any]) -> Dict[str, int]:
    """
    Retorna o número de tentativas de trancar portas enquanto abertas.
    Este dado vem diretamente do estado do objeto, não dos logs.
    Usa FILTER para pegar as portas e DICT COMPREHENSION para montar o relatório.
    """
    # 1. USA FILTER para obter apenas os dispositivos que são Portas
    portas = filter(lambda d: isinstance(d, Porta), dispositivos)
    
    # 2. USA DICT COMPREHENSION para criar o dicionário de resultado
    report = {
        porta.id: porta.tentativas_invalidas
        for porta in portas if porta.tentativas_invalidas > 0
    }
    
    return report