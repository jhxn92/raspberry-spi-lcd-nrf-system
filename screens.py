from ui import header, menu, footer, body_text

MENU_OPTIONS = ["Enviar", "Receber", "Sistema"]

def home(draw, selected):
    header(draw, "Home")
    menu(draw, MENU_OPTIONS, selected)
    footer(draw, "DS4: X entra | O volta")

def send_screen(draw, status_text="Pronto para enviar"):
    header(draw, "Enviando")
    body_text(draw, "Mensagem teste", 42, (255, 255, 255))
    body_text(draw, status_text, 64, (0, 255, 0))
    footer(draw, "OPTIONS envia")

def receive_screen(draw, last_msg):
    header(draw, "Recebendo")
    body_text(draw, "Ultima mensagem:", 38, (180, 180, 180))
    body_text(draw, last_msg[:18], 62, (255, 255, 0))
    footer(draw, "SHARE abre esta tela")

def system_screen(draw, radio_ok, gamepad_name):
    header(draw, "Sistema")
    body_text(draw, f"NRF: {'OK' if radio_ok else 'FALHA'}", 40, (0, 255, 255) if radio_ok else (255, 80, 80))
    body_text(draw, "CTRL:", 62, (180, 180, 180))
    body_text(draw, (gamepad_name or "Nao detectado")[:18], 80, (255, 255, 255))
    footer(draw, "LCD + NRF + DS4")
