import time
import board
import digitalio
import busio
import adafruit_rgb_display.st7735 as st7735

import screens
from ui import create_canvas
from nrf_module import init_nrf, send_message, receive_message
from gamepad import GamepadReader

spi = busio.SPI(clock=board.SCLK, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D24)
rst = digitalio.DigitalInOut(board.D25)

disp = st7735.ST7735R(
    spi,
    cs=cs,
    dc=dc,
    rst=rst,
    width=128,
    height=160,
    rotation=90,
)

menu_index = 0
current_screen = "home"
last_msg = "Nenhuma"
send_status = "Pronto"
radio_ok = init_nrf()
gamepad = GamepadReader()
gamepad_name = gamepad.name

def render():
    image, draw = create_canvas()
    if current_screen == "home":
        screens.home(draw, menu_index)
    elif current_screen == "send":
        screens.send_screen(draw, send_status)
    elif current_screen == "receive":
        screens.receive_screen(draw, last_msg)
    elif current_screen == "system":
        screens.system_screen(draw, radio_ok, gamepad_name)
    disp.image(image)

while True:
    if current_screen == "receive":
        msg = receive_message()
        if msg:
            last_msg = msg

    render()
    action = gamepad.poll_action()

    if action is None:
        time.sleep(0.03)
        continue

    if current_screen == "home":
        if action == "up":
            menu_index = (menu_index - 1) % len(screens.MENU_OPTIONS)
        elif action == "down":
            menu_index = (menu_index + 1) % len(screens.MENU_OPTIONS)
        elif action == "select":
            if menu_index == 0:
                current_screen = "send"
            elif menu_index == 1:
                current_screen = "receive"
            elif menu_index == 2:
                current_screen = "system"
        elif action == "send":
            ok = send_message("Ola do Raspberry!")
            send_status = "Enviado!" if ok else "Falha no envio"
            current_screen = "send"
        elif action == "receive":
            current_screen = "receive"
    else:
        if action == "back":
            current_screen = "home"
        elif current_screen == "send" and action in ("select", "send"):
            ok = send_message("Ola do Raspberry!")
            send_status = "Enviado!" if ok else "Falha no envio"
        elif current_screen == "receive" and action == "receive":
            msg = receive_message()
            if msg:
                last_msg = msg

    time.sleep(0.03)
