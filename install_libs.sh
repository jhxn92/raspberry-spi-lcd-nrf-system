#!/bin/bash

set -e

PROJECT_DIR="/home/balancerec/raspberry-spi-lcd-nrf-system"

echo "📂 Entrando no projeto..."
cd "$PROJECT_DIR"

echo "🐍 Ativando ambiente virtual..."
source venv/bin/activate

echo "⬆️ Atualizando pip..."
pip install --upgrade pip

echo "🔧 Instalando dependências do sistema (RF24 e evdev)..."
sudo apt update
sudo apt install -y python3-dev libboost-python-dev libboost-thread-dev joystick evtest

echo "📦 Instalando bibliotecas Python..."

pip install \
adafruit-blinka \
adafruit-circuitpython-rgb-display \
Pillow \
pyRF24 \
evdev

echo "✅ Instalação concluída com sucesso!"
