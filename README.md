# Raspberry Pi Embedded UI System

Projeto de sistema embarcado com interface gráfica em LCD SPI e comunicação RF usando NRF24L01, com controle via DualShock 4.

## Visão Geral

Este projeto utiliza um Raspberry Pi 3 Model B para criar um sistema embarcado com:
- Display TFT 1.8" 128x160 com driver ST7735/ST7735S
- Módulo NRF24L01 PA+LNA
- Controle de PS4 (DualShock 4) via Bluetooth
- Interface gráfica custom em Python
- DietPi como sistema operacional

## Hardware Utilizado

- Raspberry Pi 3 Model B
- Display TFT 1.8" 128x160 (ST7735/ST7735S)
- NRF24L01 PA+LNA
- Capacitor eletrolítico 10µF a 100µF entre VCC e GND do NRF
- Controle PS4 (DualShock 4)

## Pinagem Completa

### SPI compartilhado

| Função | GPIO | Pino físico |
|---|---:|---:|
| SCK | GPIO11 | 23 |
| MOSI | GPIO10 | 19 |
| MISO | GPIO9 | 21 |

### TFT LCD ST7735

| LCD | Raspberry Pi | GPIO | Pino físico | Cor |
|---|---|---:|---:|---|
| GND | GND | - | 6 | Preto |
| VCC | 3.3V | - | 1 | Vermelho
| SCL | SCK | GPIO11 | 23 | Amarelo |
| SDA | MOSI | GPIO10 | 19 | Verde |
| CS | CE0 | GPIO8 | 24 | Laranja |
| DC | GPIO24 | GPIO24 | 18 | Branco |
| RES | GPIO25 | GPIO25 | 22 | Azul |
| BL | 3.3V | - | 17 ou 1 | Branco |

### NRF24L01 PA+LNA

| NRF | Raspberry Pi | GPIO | Pino físico | Cor |
|---|---|---:|---:|---|
| GND | GND | - | 6 | Preto |
| VCC | 3.3V | - | 1 ou 17 | Vermelho |
| CE | GPIO17 | GPIO17 | 11 | Amarelo |
| CSN | CE1 | GPIO7 | 26 | Laranja |
| SCK | SCK | GPIO11 | 23 | Verde |
| MOSI | MOSI | GPIO10 | 19 | Azul |
| MISO | MISO | GPIO9 | 21 | Cinza |
| IRQ | GPIO27  | GPIO27 | 13 | Branco |

## Observações Importantes

- O barramento SPI é compartilhado entre LCD e NRF.
- LCD usa CE0 (GPIO8) e NRF usa CE1 (GPIO7).
- O LCD não usa MISO.
- O NRF24L01 PA+LNA deve operar em 3.3V, nunca em 5V.
- O capacitor do NRF deve ser instalado o mais perto possível do módulo.
- O BL do display deve estar ligado em 3.3V, senão a tela pode ficar preta.

## Diretório do Projeto

```bash
/home/balancerec/Projetos
```

## Estrutura do Projeto

```text
Projetos/
├── main.py
├── ui.py
├── screens.py
├── nrf_module.py
├── gamepad.py
├── run.sh
├── install.sh
├── requirements.txt
└── README.md
```

## Bibliotecas Python

- adafruit-blinka
- adafruit-circuitpython-rgb-display
- Pillow
- pyRF24
- evdev

## Preparação do Ambiente

### Instalar ambiente virtual

```bash
sudo apt update
sudo apt install python3-venv python3-dev python3-libgpiod -y
cd /home/balancerec/raspberry-spi-lcd-nrf-system
python3 -m venv venv
source venv/bin/activate
```

### Instalar dependências Python

```bash
pip install -r requirements.txt
```

## Ativar SPI no DietPi

```bash
sudo dietpi-config
```

Depois:
- Advanced Options
- SPI
- Enable

Reinicie o Raspberry Pi.

## Parear o controle de PS4

```bash
sudo bluetoothctl
```

Dentro do prompt:

```text
power on
agent on
default-agent
scan on
```

Coloque o controle em modo de pareamento segurando `PS + SHARE`.

Depois use:

```text
pair MAC_DO_CONTROLE
trust MAC_DO_CONTROLE
connect MAC_DO_CONTROLE
```

## Encontrar o evento do controle

```bash
python3 gamepad.py --list
```

## Execução

```bash
cd /home/balancerec/raspberry-spi-lcd-nrf-system
source venv/bin/activate
python3 main.py
```

Ou:

```bash
./run.sh
```

## Controles padrão do DualShock 4

| Botão | Ação |
|---|---|
| D-pad cima | mover seleção para cima |
| D-pad baixo | mover seleção para baixo |
| X (BTN_SOUTH) | selecionar |
| O (BTN_EAST) | voltar |
| OPTIONS (BTN_START) | enviar mensagem teste |
| SHARE (BTN_SELECT) | tela de recepção |

## Telas atuais

- Home
- Send
- Receive
- System Info
