import argparse
import sys
from typing import Dict, Any

from .hub import HubAutomacao, TIPO_CLASSE_MAP
from .observers import ConsoleObserver
from .logger import CSVLogger
from . import relatorios
from .erros import DispositivoNaoEncontradoError, ComandoInvalidoError, AtributoInvalidoError
from .dispositivos import TipoDispositivo
from smart_home.dispositivos.luz import Luz, Cor as CorLuz
from smart_home.dispositivos.tomada import Tomada
from smart_home.dispositivos.tv import Tv
from smart_home.dispositivos.microondas import Microondas
from smart_home.dispositivos.porta import Porta 

def exibir_menu():
    """Exibe o menu principal da CLI."""
    print("\n=== SMART HOME HUB ===")
    print("1. Listar dispositivos")
    print("2. Mostrar dispositivo")
    print("3. Executar comando em dispositivo")
    print("4. Alterar atributo de dispositivo")
    print("5. Executar rotina")
    print("6. Gerar relatorio")
    print("7. Salvar configuracao")
    print("8. Adicionar dispositivo")
    print("9. Remover dispositivo")
    print("10. Sair")
    return input("Escolha uma opcao: ")

def obter_argumentos_comando(comando: str) -> Dict[str, Any]:
    """Pede ao usuário os argumentos necessários para comandos específicos."""
    args = {}
    if comando == "definir_brilho":
        while True:
            try:
                brilho = int(input("  - brilho (0-100): "))
                args['brilho'] = brilho
                break
            except ValueError:
                print("ERRO: Brilho deve ser um número inteiro.")
    elif comando == "definir_cor":
        while True:
            cores_disponiveis = [c.name for c in CorLuz]
            cor_str = input(f"  - cor {cores_disponiveis}: ").upper()
            if cor_str in cores_disponiveis:
                args['cor'] = CorLuz[cor_str]
                break
            else:
                print(f"ERRO: Cor inválida. Escolha uma das opções: {cores_disponiveis}")
    return args
def main():
    """Função principal que executa a CLI do Smart Home Hub."""
    parser = argparse.ArgumentParser(description="Smart Home Hub CLI")
    parser.add_argument(
        '--config', type=str, default='smart_home/data/configuracao.json',
        help='Caminho para o arquivo de configuracao JSON.'
    )
    args = parser.parse_args()

    
    # Define os caminhos a partir da raiz do projeto, onde o comando é executado
    CONFIG_FILE = args.config
    LOG_FILE = 'smart_home/data/eventos.csv'

    # --- INICIALIZAÇÃO DO SISTEMA ---
    try:
        hub = HubAutomacao(CONFIG_FILE)
        logger = CSVLogger(LOG_FILE)
        hub.adicionar_observer(ConsoleObserver())
        hub.adicionar_observer(logger)
    except Exception as e:
        print(f"ERRO CRÍTICO ao inicializar o Hub: {e}")
        sys.exit(1)

    # --- LOOP PRINCIPAL DA APLICAÇÃO ---
    while True:
        try:
            opcao = exibir_menu()

            if opcao == '1': # Listar dispositivos
                # (Sem alterações aqui)
                dispositivos = hub.listar_dispositivos()
                if not dispositivos:
                    print("\nNenhum dispositivo cadastrado.")
                else:
                    print("\n--- Dispositivos Cadastrados ---")
                    for dev in dispositivos:
                        print(f"  ID: {dev.id:<15} | Nome: {dev.nome:<20} | Tipo: {dev.tipo.value:<10} | Estado: {dev.state}")
                    print("---------------------------------")
            
            # As opções 2 a 5 não precisam de alteração
            elif opcao == '2':
                id_dev = input("ID do dispositivo: ")
                dev = hub.get_dispositivo(id_dev)
                print("\n--- Detalhes do Dispositivo ---")
                print(f"  ID:    {dev.id}")
                print(f"  Nome:  {dev.nome}")
                print(f"  Tipo:  {dev.tipo.value}")
                estado_info = dev.get_estado_dict()
                print(f"  Estado: {estado_info['estado']}")
                if estado_info['atributos']:
                    print("  Atributos:")
                    for attr, valor in estado_info['atributos'].items():
                        print(f"    - {attr}: {valor}")
                print("---------------------------------")

            elif opcao == '3': # Executar comando em dispositivo
                id_dev = input("ID do dispositivo: ")
                dev = hub.get_dispositivo(id_dev)

                # Pega a lista de comandos (triggers) disponíveis a partir do estado atual do dispositivo
                comandos_disponiveis = dev.maquina.get_triggers(dev.state)

                print(f"\n--- Comandos para '{dev.nome}' (Estado atual: '{dev.state}') ---")
                if not comandos_disponiveis:
                    print("Nenhum comando disponível neste estado.")
                    continue
                
                print(f"Comandos disponíveis: {', '.join(comandos_disponiveis)}")
                comando = input("Comando a executar: ")

                # O resto da lógica para pegar argumentos e executar permanece o mesmo
                args_comando = obter_argumentos_comando(comando)
                hub.executar_comando(id_dev, comando, args_comando)

            elif opcao == '4': # Alterar atributo de dispositivo
                id_dev = input("ID do dispositivo: ")
                dev = hub.get_dispositivo(id_dev)

                print(f"\n--- Alterar Atributo para '{dev.nome}' ({dev.tipo.value}) ---")

                # Lógica específica para cada tipo de dispositivo
                if isinstance(dev, Luz):
                    print("Atributos alteraveis:")
                    print("  1. brilho")
                    print("  2. cor")
                    attr_escolha = input("Escolha o atributo: ")

                    if attr_escolha == '1':
                        attr_nome = 'brilho'
                        while True:  # Loop para validar a entrada
                            try:
                                valor_str = input(f"Novo valor para brilho (0-100) [atual: {dev.brilho}]: ")
                                novo_valor = int(valor_str)
                                dev.brilho = novo_valor  # Usa o descriptor para validar e atribuir
                                break  # Sai do loop se o valor for válido
                            except (ValueError, AtributoInvalidoError) as e:
                                print(f"ERRO: {e}. Tente novamente.")

                    elif attr_escolha == '2':
                        attr_nome = 'cor'
                        cores_disponiveis = [c.name for c in CorLuz]
                        while True: # Loop para validar a entrada
                            try:
                                print(f"Cores disponiveis: {cores_disponiveis}")
                                valor_str = input(f"Nova cor [atual: {dev.cor.name}]: ").upper()
                                novo_valor = CorLuz[valor_str]
                                dev.cor = novo_valor # Usa o descriptor
                                break
                            except KeyError:
                                print(f"ERRO: Cor inválida. Escolha uma das opções.")

                    else:
                        print("Opção de atributo inválida.")
                        continue # Volta para o menu principal

                elif isinstance(dev, (Tomada, Tv, Microondas)):
                    attr_nome = 'potencia_w'
                    print(f"Atributo alteravel: potencia_w")
                    while True: # Loop para validar a entrada
                        try:
                            valor_str = input(f"Novo valor para potencia_w (W) [atual: {dev.potencia_w}]: ")
                            novo_valor = int(valor_str)
                            dev.potencia_w = novo_valor # Usa o descriptor
                            break
                        except (ValueError, AtributoInvalidoError) as e:
                            print(f"ERRO: {e}. Tente novamente.")

                else:
                    # Para dispositivos como Porta ou Alarme, que não têm atributos configuráveis
                    print(f"O dispositivo '{dev.nome}' não possui atributos alteráveis pelo usuário.")
                    continue

                print(f"Atributo '{attr_nome}' de '{dev.id}' alterado com sucesso.")

            elif opcao == '5': # Executar rotina
                rotinas_disponiveis = hub.listar_rotinas()

                print("\n--- Executar Rotina ---")
                if not rotinas_disponiveis:
                    print("Nenhuma rotina foi configurada no arquivo JSON.")
                    continue  # Volta para o menu principal

                print(f"Rotinas disponíveis: {', '.join(rotinas_disponiveis)}")
                nome_rotina = input("Nome da rotina a executar: ")

                
                # verificação extra de tratamento.
                if nome_rotina in rotinas_disponiveis:
                    hub.executar_rotina(nome_rotina)
                else:
                    print(f"Rotina '{nome_rotina}' não encontrada.")

            elif opcao == '6': # --- BLOCO DE RELATÓRIOS COMPLETO ---
                print("\n--- GERAR RELATORIO ---")
                print("  1. Tempo de luzes ligadas")
                print("  2. Consumo de energia por tomada")
                print("  3. Dispositivos mais usados")
                print("  4. Comandos por tipo de dispositivo")
                print("  5. Tentativas invalidas de trancar portas")
                tipo_relatorio = input("Escolha o relatorio: ")
                
                eventos = relatorios.carregar_eventos(LOG_FILE)
                dispositivos_hub = hub.listar_dispositivos()
                
                print("\n--- RESULTADO DO RELATORIO ---")
                if tipo_relatorio == '1':
                    resultado = relatorios.relatorio_tempo_luz_ligada(eventos, dispositivos_hub)
                    if not any(resultado.values()):
                        print("Nenhum dado de tempo de uso encontrado para as luzes.")
                    for luz_id, segundos in resultado.items():
                        if segundos > 0:
                            print(f"- Luz '{luz_id}': {segundos:.2f} segundos (~{segundos/60:.2f} minutos)")
                
                elif tipo_relatorio == '2':
                    resultado = relatorios.relatorio_consumo_tomada(eventos, dispositivos_hub)
                    if not any(resultado.values()):
                        print("Nenhum dado de consumo encontrado para as tomadas.")
                    for tomada_id, consumo_wh in resultado.items():
                        if consumo_wh > 0:
                            print(f"- Tomada '{tomada_id}': {consumo_wh:.4f} Wh (~{consumo_wh/1000:.4f} kWh)")

                elif tipo_relatorio == '3':
                    resultado = relatorios.relatorio_dispositivos_mais_usados(eventos)
                    if not resultado:
                        print("Nenhum evento encontrado para gerar ranking de uso.")
                    for disp_id, contagem in resultado:
                        print(f"- Dispositivo '{disp_id}': {contagem} eventos")

                elif tipo_relatorio == '4':
                    resultado = relatorios.relatorio_distribuicao_comandos_por_tipo(eventos, dispositivos_hub)
                    if not resultado:
                        print("Nenhum evento encontrado para gerar distribuição de comandos.")
                    for tipo, comandos in resultado.items():
                        comandos_str = ', '.join([f'{cmd}({num})' for cmd, num in comandos.items()])
                        print(f"- Tipo '{tipo}': {comandos_str}")

                elif tipo_relatorio == '5':
                    resultado = relatorios.relatorio_tentativas_invalidas_porta(dispositivos_hub)
                    if not resultado:
                        print("Nenhuma tentativa inválida de trancar portas registrada.")
                    for porta_id, contagem in resultado.items():
                        print(f"- Porta '{porta_id}': {contagem} tentativas invalidas")
                
                else:
                    print("Opção de relatório inválida.")
                print("---------------------------------")

            elif opcao == '7': # Salvar configuracao
                hub.salvar_configuracao()

            elif opcao == '8': # Adicionar dispositivo
                print("Tipos suportados:", ", ".join([t.name for t in TIPO_CLASSE_MAP.keys()]))
                tipo_str = input("tipo: ").upper()
                id_novo = input("id (sem espacos): ")
                nome_novo = input("nome: ")
                
                # ===== CORREÇÃO CRÍTICA APLICADA AQUI =====
                try:
                    # 1. Converte a string do tipo para o Enum correspondente
                    tipo_enum = TipoDispositivo[tipo_str]
                    # 2. Pega a classe correta do mapeamento
                    classe_dispositivo = TIPO_CLASSE_MAP.get(tipo_enum)
                except KeyError:
                    # Se o tipo digitado não existir no Enum, dá erro
                    print("ERRO: Tipo de dispositivo inválido.")
                    continue
                
                if not classe_dispositivo:
                    print(f"ERRO: A classe para o tipo '{tipo_str}' não foi encontrada no mapeamento.")
                    continue
                
                # Argumentos específicos de cada tipo
                kwargs = {'id': id_novo, 'nome': nome_novo}
                if tipo_enum == TipoDispositivo.LIGHT:
                    kwargs['brilho'] = int(input("brilho (0-100) [50]: ") or 50)
                    cor_str = input("cor [QUENTE/FRIA/NEUTRA] [NEUTRA]: ").upper() or 'NEUTRA'
                    kwargs['cor'] = CorLuz[cor_str]
                elif tipo_enum in [TipoDispositivo.OUTLET, TipoDispositivo.MICROWAVE, TipoDispositivo.TV]:
                    kwargs['potencia_w'] = int(input("potencia_w [100]: ") or 100)

                novo_dispositivo = classe_dispositivo(**kwargs)
                hub.adicionar_dispositivo(novo_dispositivo)

            elif opcao == '9': # Remover dispositivo
                # (Sem alterações aqui)
                id_remover = input("ID do dispositivo a ser removido: ")
                hub.remover_dispositivo(id_remover)

            elif opcao == '10': # Sair
                # (Sem alterações aqui)
                hub.salvar_configuracao()
                logger.close()
                print("Saindo...")
                break
            else:
                print("\nOpção inválida, tente novamente.")

        except (DispositivoNaoEncontradoError, ComandoInvalidoError, AtributoInvalidoError, KeyError, ValueError) as e:
            print(f"\nERRO: {e}")
        except Exception as e:
            print(f"\nERRO INESPERADO: {e.__class__.__name__}: {e}")

if __name__ == '__main__':
    main()