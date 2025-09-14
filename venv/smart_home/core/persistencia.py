# smart_home/core/persistencia.py

import json
from .erros import ConfiguracaoInvalidaError

def carregar_de_json(caminho_arquivo: str) -> dict:
    """Carrega dados de um arquivo JSON."""
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Se o arquivo não existe, é um estado válido (primeira execução).
        # Retorna um dicionário vazio para o Hub lidar com isso.
        return {}
    except json.JSONDecodeError as e:
        # Se o arquivo existe mas é inválido, lança uma exceção personalizada.
        raise ConfiguracaoInvalidaError(f"Erro ao decodificar o JSON em '{caminho_arquivo}': {e}")


def salvar_em_json(caminho_arquivo: str, dados: dict):
    """Salva dados em um arquivo JSON de forma segura."""
    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"ERRO: Não foi possível salvar o arquivo de configuração em '{caminho_arquivo}': {e}")