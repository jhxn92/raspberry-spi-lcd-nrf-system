#!/bin/bash
set -e

PROJECT_DIR="/home/balancerec/Projetos"

sudo apt update
sudo apt install -y python3-venv python3-dev python3-libgpiod bluetooth bluez

mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Instalacao concluida."
echo "Ative o SPI em: sudo dietpi-config"
echo "Liste controles em: python3 gamepad.py --list"
