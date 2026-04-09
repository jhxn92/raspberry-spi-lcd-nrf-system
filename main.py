import time
import board
import digitalio
import busio
from PIL import Image
import adafruit_rgb_display.st7735 as st7735

import screens
from ui import create_canvas, create_offscreen, WIDTH, HEIGHT
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

radio_ok = init_nrf()
gamepad = GamepadReader()
gamepad_name = gamepad.name

bt_status = "Conectado" if gamepad_name else "Desconectado"
nrf_status = "OK" if radio_ok else "Falha"

last_msg = "Nenhuma"
send_status = "Pronto"
lcd_test_phase = 0

current_screen = "home"
screen_stack = []

menu_indices = {
    "home": 0,
    "bluetooth_menu": 0,
    "nrf_menu": 0,
    "lcd_menu": 0,
    "system_menu": 0,
}

menu_highlight_y = {
    "home": 30,
    "bluetooth_menu": 30,
    "nrf_menu": 30,
    "lcd_menu": 30,
    "system_menu": 30,
}

MENU_START_Y = 30
MENU_STEP = 22


def push_screen(screen_name: str):
    global current_screen
    screen_stack.append(current_screen)
    old_screen = current_screen
    current_screen = screen_name
    animate_screen_transition(old_screen, current_screen, direction="left")


def pop_screen():
    global current_screen
    old_screen = current_screen
    if screen_stack:
        current_screen = screen_stack.pop()
    else:
        current_screen = "home"
    animate_screen_transition(old_screen, current_screen, direction="right")


def menu_length(screen_name: str) -> int:
    if screen_name == "home":
        return len(screens.HOME_MENU)
    if screen_name == "bluetooth_menu":
        return len(screens.BLUETOOTH_MENU)
    if screen_name == "nrf_menu":
        return len(screens.NRF_MENU)
    if screen_name == "lcd_menu":
        return len(screens.LCD_MENU)
    if screen_name == "system_menu":
        return len(screens.SYSTEM_MENU)
    return 0


def target_highlight_y(screen_name: str) -> int:
    idx = menu_indices.get(screen_name, 0)
    return MENU_START_Y + idx * MENU_STEP


def move_menu(direction: str):
    if current_screen not in menu_indices:
        return

    total = menu_length(current_screen)
    if total <= 0:
        return

    if direction == "up":
        menu_indices[current_screen] = (menu_indices[current_screen] - 1) % total
    elif direction == "down":
        menu_indices[current_screen] = (menu_indices[current_screen] + 1) % total


def animate_menu_highlight():
    if current_screen not in menu_highlight_y:
        return

    target = target_highlight_y(current_screen)
    current = menu_highlight_y[current_screen]

    if current == target:
        return

    steps = 5
    for i in range(1, steps + 1):
        interp = current + (target - current) * i / steps
        menu_highlight_y[current_screen] = interp
        render()
        time.sleep(0.01)

    menu_highlight_y[current_screen] = target


def draw_screen(draw, screen_name: str):
    if screen_name == "home":
        screens.home(draw, menu_indices["home"], highlight_y=menu_highlight_y["home"])

    elif screen_name == "bluetooth_menu":
        screens.bluetooth_menu(
            draw,
            menu_indices["bluetooth_menu"],
            bt_status,
            highlight_y=menu_highlight_y["bluetooth_menu"],
        )

    elif screen_name == "bluetooth_status":
        screens.bluetooth_status(draw, bt_status, gamepad_name)

    elif screen_name == "bluetooth_devices":
        devices = [gamepad_name] if gamepad_name else []
        screens.bluetooth_devices(draw, devices, 0)

    elif screen_name == "nrf_menu":
        screens.nrf_menu(
            draw,
            menu_indices["nrf_menu"],
            nrf_status,
            highlight_y=menu_highlight_y["nrf_menu"],
        )

    elif screen_name == "nrf_status":
        screens.nrf_status(draw, radio_ok, last_msg)

    elif screen_name == "nrf_send":
        screens.nrf_send(draw, send_status)

    elif screen_name == "nrf_receive":
        screens.nrf_receive(draw, last_msg)

    elif screen_name == "lcd_menu":
        screens.lcd_menu(
            draw,
            menu_indices["lcd_menu"],
            highlight_y=menu_highlight_y["lcd_menu"],
        )

    elif screen_name == "lcd_info":
        screens.lcd_info(draw)

    elif screen_name == "lcd_test":
        screens.lcd_test(draw, lcd_test_phase)

    elif screen_name == "system_menu":
        screens.system_menu(
            draw,
            menu_indices["system_menu"],
            highlight_y=menu_highlight_y["system_menu"],
        )

    elif screen_name == "system_summary":
        screens.system_summary(draw, gamepad_name, bt_status, nrf_status)

    elif screen_name == "system_controller":
        screens.system_controller(draw, gamepad_name)

    else:
        screens.home(draw, menu_indices["home"], highlight_y=menu_highlight_y["home"])


def render():
    image, draw = create_canvas()
    draw_screen(draw, current_screen)
    disp.image(image)


def render_to_image(screen_name: str):
    image, draw = create_offscreen()
    draw_screen(draw, screen_name)
    return image


def animate_screen_transition(old_screen: str, new_screen: str, direction="left"):
    old_img = render_to_image(old_screen)
    new_img = render_to_image(new_screen)

    steps = 8

    for i in range(steps + 1):
        frame = Image.new("RGB", (WIDTH, HEIGHT), (8, 8, 10))
        progress = i / steps

        if direction == "left":
            old_x = int(-WIDTH * progress)
            new_x = int(WIDTH - WIDTH * progress)
        else:
            old_x = int(WIDTH * progress)
            new_x = int(-WIDTH + WIDTH * progress)

        frame.paste(old_img, (old_x, 0))
        frame.paste(new_img, (new_x, 0))
        disp.image(frame)
        time.sleep(0.012)


def do_nrf_send():
    global send_status, current_screen
    send_status = "Enviando..."
    current_screen = "nrf_send"
    render()
    ok = send_message("Ola do Raspberry!")
    send_status = "Enviado!" if ok else "Falha no envio"


def update_receive():
    global last_msg
    msg = receive_message()
    if msg:
        last_msg = msg


def handle_select():
    global current_screen, lcd_test_phase

    if current_screen == "home":
        idx = menu_indices["home"]
        if idx == 0:
            push_screen("bluetooth_menu")
        elif idx == 1:
            push_screen("nrf_menu")
        elif idx == 2:
            push_screen("lcd_menu")
        elif idx == 3:
            push_screen("system_menu")

    elif current_screen == "bluetooth_menu":
        idx = menu_indices["bluetooth_menu"]
        if idx == 0:
            push_screen("bluetooth_status")
        elif idx == 1:
            push_screen("bluetooth_devices")
        elif idx == 2:
            pop_screen()

    elif current_screen == "nrf_menu":
        idx = menu_indices["nrf_menu"]
        if idx == 0:
            push_screen("nrf_status")
        elif idx == 1:
            push_screen("nrf_send")
        elif idx == 2:
            push_screen("nrf_receive")
        elif idx == 3:
            pop_screen()

    elif current_screen == "lcd_menu":
        idx = menu_indices["lcd_menu"]
        if idx == 0:
            push_screen("lcd_info")
        elif idx == 1:
            push_screen("lcd_test")
        elif idx == 2:
            pop_screen()

    elif current_screen == "system_menu":
        idx = menu_indices["system_menu"]
        if idx == 0:
            push_screen("system_summary")
        elif idx == 1:
            push_screen("system_controller")
        elif idx == 2:
            pop_screen()

    elif current_screen == "nrf_send":
        do_nrf_send()

    elif current_screen == "nrf_receive":
        update_receive()

    elif current_screen == "lcd_test":
        lcd_test_phase = (lcd_test_phase + 1) % 4


def handle_send_action():
    if current_screen in ("home", "nrf_menu", "nrf_send"):
        do_nrf_send()


def handle_receive_action():
    global current_screen
    if current_screen in ("home", "nrf_menu"):
        current_screen = "nrf_receive"
        render()
    elif current_screen == "nrf_receive":
        update_receive()


def handle_back():
    if current_screen == "home":
        return
    pop_screen()


print("Sistema iniciando...")
print(f"Controle detectado: {gamepad_name}")
print(f"Bluetooth: {bt_status}")
print(f"NRF inicializado: {radio_ok}")

try:
    while True:
        if current_screen == "nrf_receive":
            update_receive()

        render()
        action = gamepad.poll_action()
        print("ACAO:", action)
        
        if action is None:
            time.sleep(0.03)
            continue

        if action == "up":
            move_menu("up")
            animate_menu_highlight()

        elif action == "down":
            move_menu("down")
            animate_menu_highlight()

        elif action == "select":
            handle_select()

        elif action == "back":
            handle_back()

        elif action == "send":
            handle_send_action()

        elif action == "receive":
            handle_receive_action()

        time.sleep(0.03)

except KeyboardInterrupt:
    print("\\nSaindo do sistema...")
