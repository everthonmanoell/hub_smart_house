class SmartHomeError(Exception):
    """Classe base para exceções do projeto."""
    pass

class DispositivoNaoEncontradoError(SmartHomeError):
    """Lançada quando um dispositivo com o ID fornecido não é encontrado."""
    pass

class ComandoInvalidoError(SmartHomeError):
    """Lançada quando um comando inválido é enviado a um dispositivo."""
    pass

class AtributoInvalidoError(SmartHomeError):
    """Lançada quando um atributo inválido é definido para um dispositivo."""
    pass

class ConfiguracaoInvalidaError(SmartHomeError):
    """Lançada quando o arquivo de configuração é inválido."""
    pass