from ui import (
    header,
    footer,
    menu,
    body_text,
    info_label,
    status_pill,
    card,
    section_title,
    center_text,
    empty_state,
    progress_bar,
)

HOME_MENU = ["Bluetooth", "NRF", "LCD", "Sistema"]
BLUETOOTH_MENU = ["Status", "Dispositivos", "Voltar"]
NRF_MENU = ["Status", "Enviar teste", "Receber", "Voltar"]
LCD_MENU = ["Info", "Teste de tela", "Voltar"]
SYSTEM_MENU = ["Resumo", "Controle", "Voltar"]


def home(draw, selected: int, highlight_y=None) -> None:
    header(draw, "Home")
    body_text(draw, "Painel principal", 22, (150, 150, 160))
    menu(draw, HOME_MENU, selected, highlight_y=highlight_y)
    footer(draw, "X entra | O volta")


def bluetooth_menu(draw, selected: int, bt_status: str = "Desconhecido", highlight_y=None) -> None:
    header(draw, "Bluetooth")
    status_pill(draw, 8, 22, bt_status, ok=(bt_status == "Conectado"))
    menu(draw, BLUETOOTH_MENU, selected, highlight_y=highlight_y)
    footer(draw, "Conexoes e status")


def bluetooth_status(draw, bt_status: str, controller_name: str | None = None) -> None:
    header(draw, "BT Status")
    info_label(draw, "Bluetooth", bt_status, 24)
    info_label(draw, "Controle", controller_name or "Nao detectado", 58)
    footer(draw, "O volta")


def bluetooth_devices(draw, devices: list[str], selected: int = 0) -> None:
    header(draw, "BT Devices")

    if not devices:
        empty_state(draw, "Nenhum dispositivo", "O volta")
        footer(draw, "O volta")
        return

    section_title(draw, "Dispositivos", 24)

    y = 38
    for i, dev in enumerate(devices[:4]):
        if i == selected:
            card(draw, "Selecionado", [dev], y=y - 6, h=28)
        else:
            body_text(draw, dev[:22], y, (210, 210, 210))
        y += 22

    footer(draw, "X seleciona | O volta")


def nrf_menu(draw, selected: int, nrf_status: str = "Desconhecido", highlight_y=None) -> None:
    header(draw, "NRF24")
    status_pill(draw, 8, 22, nrf_status, ok=(nrf_status == "OK"))
    menu(draw, NRF_MENU, selected, highlight_y=highlight_y)
    footer(draw, "Radio e mensagens")


def nrf_status(draw, radio_ok: bool, last_msg: str = "Nenhuma") -> None:
    header(draw, "NRF Status")
    status_pill(draw, 8, 22, "OK" if radio_ok else "FALHA", ok=radio_ok)
    card(draw, "Ultima mensagem", [last_msg or "Nenhuma"], y=42, h=36)
    footer(draw, "O volta")


def nrf_send(draw, send_status: str = "Pronto") -> None:
    header(draw, "NRF Enviar")
    card(draw, "Mensagem", ["Ola do Raspberry!"], y=28, h=34)

    color = (0, 255, 0) if "Enviado" in send_status else (255, 210, 80)
    body_text(draw, send_status, 74, color)

    if "Enviando" in send_status:
        progress_bar(draw, 8, 94, 144, 10, 0.65)

    footer(draw, "OPTIONS envia | O volta")


def nrf_receive(draw, last_msg: str = "Nenhuma") -> None:
    header(draw, "NRF Receber")
    card(draw, "Recepcao", ["Aguardando dados...", last_msg or "Nenhuma"], y=28, h=48)
    footer(draw, "SHARE atualiza | O volta")


def lcd_menu(draw, selected: int, highlight_y=None) -> None:
    header(draw, "LCD")
    body_text(draw, "Diagnostico de tela", 22, (150, 150, 160))
    menu(draw, LCD_MENU, selected, highlight_y=highlight_y)
    footer(draw, "Tela e teste")


def lcd_info(draw) -> None:
    header(draw, "LCD Info")
    info_label(draw, "Driver", "ST7735", 24)
    info_label(draw, "Resolucao", "160x128", 58)
    info_label(draw, "Interface", "SPI / CE0", 92)
    footer(draw, "O volta")


def lcd_test(draw, phase: int = 0) -> None:
    header(draw, "LCD Teste")

    colors = [
        ((255, 0, 0), "Vermelho"),
        ((0, 255, 0), "Verde"),
        ((0, 0, 255), "Azul"),
        ((255, 255, 255), "Branco"),
    ]

    color, name = colors[phase % len(colors)]
    draw.rounded_rectangle((18, 30, 142, 88), radius=8, fill=color, outline=(60, 60, 60))
    center_text(draw, name, 96, (230, 230, 230))
    footer(draw, "X troca cor | O volta")


def system_menu(draw, selected: int, highlight_y=None) -> None:
    header(draw, "Sistema")
    body_text(draw, "Resumo do dispositivo", 22, (150, 150, 160))
    menu(draw, SYSTEM_MENU, selected, highlight_y=highlight_y)
    footer(draw, "Info e controle")


def system_summary(draw, gamepad_name: str | None, bt_status: str, nrf_status: str) -> None:
    header(draw, "Resumo")
    info_label(draw, "Bluetooth", bt_status, 22)
    info_label(draw, "NRF", nrf_status, 52)
    info_label(draw, "Controle", gamepad_name or "Nao detectado", 82)
    footer(draw, "O volta")


def system_controller(draw, gamepad_name: str | None) -> None:
    header(draw, "Controle")
    card(
        draw,
        "DualShock 4",
        [
            (gamepad_name or "Nao detectado")[:22],
            "D-pad e analogicos",
            "X entra | O volta",
        ],
        y=28,
        h=54,
    )
    footer(draw, "O volta")
