#!/bin/bash
# Script para criar a estrutura de diretórios e arquivos do projeto smart_home

# Criar a pasta raiz
mkdir -p smart_home

# Entrar na pasta raiz
cd smart_home || exit

# Criar arquivos principais
touch README.md requirements.txt

# Criar pasta data e arquivos de exemplo
mkdir -p data
touch data/configuracao.exemplo.json data/eventos.exemplo.csv data/relatorio.exemplo.csv

# Criar estrutura do pacote smart_home
mkdir -p smart_home/core smart_home/dispositivos
touch smart_home/__init__.py

# Criar arquivos dentro de core
touch smart_home/core/cli.py \
      smart_home/core/hub.py \
      smart_home/core/dispositivos.py \
      smart_home/core/eventos.py \
      smart_home/core/observers.py \
      smart_home/core/logger.py \
      smart_home/core/persistencia.py \
      smart_home/core/erros.py

# Criar arquivos de dispositivos
touch smart_home/dispositivos/porta.py \
      smart_home/dispositivos/luz.py \
      smart_home/dispositivos/tomada.py \
      smart_home/dispositivos/cafeteira.py

# Exibir a árvore criada
echo "Estrutura criada com sucesso:"
tree .
