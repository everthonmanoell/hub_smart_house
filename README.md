# Smart Home Hub (Hub de Automação Residencial)

Este projeto é um sistema de automação residencial em Python chamado **Smart Home Hub**. Ele gerencia dispositivos inteligentes (luzes, portas, tomadas, alarmes, etc.) via uma **CLI** e aplica conceitos de OOP, padrões de projeto, FSM (`transitions`), descritores, exceções, I/O (JSON/CSV) e programação funcional.

---

## Índice

- [Smart Home Hub (Hub de Automação Residencial)](#smart-home-hub-hub-de-automação-residencial)
  - [Índice](#índice)
  - [Objetivo](#objetivo)
  - [Funcionalidades principais](#funcionalidades-principais)
  - [Estrutura do projeto](#estrutura-do-projeto)
  - [Conceitos e tecnologias aplicadas](#conceitos-e-tecnologias-aplicadas)
  - [Instalação](#instalação)
  - [Como executar](#como-executar)
  - [Guia rápido da CLI](#guia-rápido-da-cli)
  - [Formato dos arquivos](#formato-dos-arquivos)
    - [`configuracao.json` (exemplo)](#configuracaojson-exemplo)
    - [`eventos.csv` (exemplo)](#eventoscsv-exemplo)
    - [Relatórios CSV](#relatórios-csv)
  - [Testes rápidos](#testes-rápidos)
  - [Contribuição](#contribuição)
  - [Autor](#autor)

---

## Objetivo

Criar um hub de automação residencial que permita:

* Gerenciar dispositivos (adicionar, remover, listar, visualizar).
* Enviar comandos que disparam FSMs dos dispositivos.
* Executar rotinas (sequência de comandos pré-configurada).
* Persistir/recuperar estado via JSON.
* Registrar eventos de transição em CSV.
* Gerar relatórios a partir dos logs (usando `map`/`filter`/`reduce`).

---

## Funcionalidades principais

* Gerenciamento de dispositivos (Luz, Porta, Tomada, Alarme, TV, etc.).
* FSMs por dispositivo (biblioteca `transitions`).
* Validação de atributos via descritores/propriedades.
* Observer (Console + Arquivo/Logger).
* Singleton para logger CSV.
* Persistência em JSON (`configuracao.json`).
* Logs de eventos em CSV (`eventos.csv`).
* Geração de relatórios (consumo, tempo ligado, ranking de uso).

---

## Estrutura do projeto

```
smart_home/
├── data/
│   ├── configuracao.json
│   └── eventos.csv
├── smart_home/
│   ├── __init__.py
│   ├── core/
│   │   ├── cli.py
│   │   ├── hub.py
│   │   ├── dispositivos.py
│   │   ├── persistencia.py
│   │   ├── logger.py
│   │   ├── observers.py
│   │   ├── relatorios.py
│   │   └── erros.py
│   ├── dispositivos/
│   │   ├── luz.py
│   │   ├── porta.py
│   │   ├── tomada.py
│   │   ├── alarme.py
│   │   └── ...
│   └── main.py
├── README.md
└── requirements.txt
```

---

## Conceitos e tecnologias aplicadas

* **OOP:** classes abstratas (`Dispositivo`), herança, polimorfismo e encapsulamento.
* **Descritores/propriedades:** validações (ex.: `brilho` 0–100, `potencia_w` ≥ 0).
* **FSM:** `transitions` para garantir transições válidas.
* **Padrões:** `Singleton` (logger CSV), `Observer` (console e arquivo).
* **I/O:** JSON para configuração/estado; CSV para logs e relatórios.
* **Programação funcional:** `map`, `filter`, `reduce`, comprehensions para relatórios.

---

## Instalação

Requisitos: **Python 3.10+**

1. Clone o repositório:

```bash
git clone https://github.com/everthonmanoell/hub_smart_house.git
cd hub_smart_house
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Como executar

Executar o ponto de entrada (CLI):

```bash
python -m smart_home.main
```

Você pode passar um arquivo de configuração customizado:

```bash
python -m smart_home.main --config data/configuracao.json
```

Ao iniciar, o Hub carrega a `configuracao.json` (se existir) e o `eventos.csv` é usado como log (ou criado quando houver o primeiro evento). Ao sair, a configuração atual é salva.

---

## Guia rápido da CLI

Menu principal (sem acentos para facilitar):

```
=== SMART HOME HUB ===
1. Listar dispositivos
2. Mostrar dispositivo
3. Executar comando em dispositivo
4. Alterar atributo de dispositivo
5. Executar rotina
6. Gerar relatorio
7. Salvar configuracao
8. Adicionar dispositivo
9. Remover dispositivo
10. Sair
Escolha uma opcao:
```

Fluxos típicos:

* **Adicionar dispositivo (8):**

  * Informe tipo (`PORTA`, `LUZ`, `TOMADA`, `ALARME`, `TV`, etc.), id, nome e atributos (ex.: brilho, cor, potencia\_w).
  * Evento de `DispositivoAdicionado` é emitido.

* **Executar comando (3):**

  * Informe `id` do dispositivo e o `comando` (ex.: `ligar`, `desligar`, `trancar`, `definir_brilho`).
  * Caso o comando aceite argumentos, informe no formato `k=v` separados por espaço.

* **Executar rotina (5):**

  * Escolha uma rotina configurada no JSON (`modo_noite`, `acordar`, ...).
  * O Hub aplica cada ação na sequência e registra eventos.

* **Gerar relatório (6):**

  * Escolha tipo de relatório (ex.: consumo por tomada, tempo que cada luz ficou ligada, dispositivos mais usados).
  * Opções adicionais podem pedir período (data inicial/final).

---

## Formato dos arquivos

### `configuracao.json` (exemplo)

```json
{
  "hub": { "nome": "Casa Exemplo", "versao": "1.0" },
  "dispositivos": [
    { "id": "porta_entrada", "tipo": "PORTA", "nome": "Porta de Entrada", "estado": "trancada", "atributos": {} },
    { "id": "luz_sala", "tipo": "LUZ", "nome": "Luz da Sala", "estado": "off", "atributos": { "brilho": 70, "cor": "QUENTE" } },
    { "id": "tomada_tv", "tipo": "TOMADA", "nome": "Tomada TV", "estado": "off", "atributos": { "potencia_w": 120 } }
  ],
  "rotinas": {
    "modo_noite": [
      { "id": "porta_entrada", "comando": "trancar" },
      { "id": "luz_sala", "comando": "desligar" }
    ],
    "acordar": [
      { "id": "luz_quarto", "comando": "ligar", "argumentos": { "brilho": 50 } },
      { "id": "cafeteira", "comando": "preparar" }
    ]
  }
}
```

### `eventos.csv` (exemplo)

Cabeçalho:

```
timestamp,id_dispositivo,evento,estado_origem,estado_destino
```

Exemplo de linhas:

```
2025-09-14T20:15:30.123456,luz_sala,ligar,off,on
2025-09-14T22:45:10.567890,luz_sala,desligar,on,off
```

### Relatórios CSV

Formato depende do relatório; ex. consumo por tomada:

```
id_dispositivo,total_wh,inicio_periodo,fim_periodo
tomada_tv,240,2025-09-01T00:00:00,2025-09-01T23:59:59
```

---

## Testes rápidos

Nos módulos (ex.: `tomada.py`, `porta.py`) há blocos:

```python
if __name__ == "__main__":
    # testes rápidos das transições e atributos
```

Use-os para validar comportamento localmente.

---

## Contribuição

1. Abra uma issue descrevendo o problema/feature.
2. Crie um branch a partir de `main`.
3. Envie um PR com descrição clara das mudanças e testes.

---

## Autor

Everthon Manoel da Silva Inácio

---

