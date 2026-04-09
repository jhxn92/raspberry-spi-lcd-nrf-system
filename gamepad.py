import sys
import time
import select
from evdev import InputDevice, list_devices, ecodes

DEFAULT_DEVICE_HINT = "Wireless Controller"


def list_gamepads():
    devices = []
    for path in list_devices():
        dev = InputDevice(path)
        devices.append((path, dev.name))
    return devices


def find_gamepad(preferred_name: str = DEFAULT_DEVICE_HINT):
    for path in list_devices():
        dev = InputDevice(path)

        if preferred_name.lower() in dev.name.lower():
            if "Motion" in dev.name:
                continue
            if "Touchpad" in dev.name:
                continue
            return dev
    return None


class GamepadReader:
    def __init__(self, preferred_name: str = DEFAULT_DEVICE_HINT):
        self.device = find_gamepad(preferred_name)
        self.name = self.device.name if self.device else None

        self.last_nav_time = 0.0
        self.nav_delay = 0.16

        self.deadzone_low = 100
        self.deadzone_high = 155

        self.last_axis_state = {
            "ABS_X": 0,
            "ABS_Y": 0,
            "ABS_RX": 0,
            "ABS_RY": 0,
            "ABS_HAT0X": 0,
            "ABS_HAT0Y": 0,
        }

    def _can_navigate(self) -> bool:
        now = time.monotonic()
        if now - self.last_nav_time >= self.nav_delay:
            self.last_nav_time = now
            return True
        return False

    def _axis_direction(self, code: str, value: int):
        # D-pad
        if code == "ABS_HAT0Y":
            if value == -1:
                return "up"
            if value == 1:
                return "down"
            return None

        if code == "ABS_HAT0X":
            if value == -1:
                return "left"
            if value == 1:
                return "right"
            return None

        # Analógicos: faixa típica central ~128
        if code in ("ABS_Y", "ABS_RY"):
            if value < self.deadzone_low:
                return "up"
            if value > self.deadzone_high:
                return "down"
            return None

        if code in ("ABS_X", "ABS_RX"):
            if value < self.deadzone_low:
                return "left"
            if value > self.deadzone_high:
                return "right"
            return None

        return None

    def _neutral_state(self, code: str, value: int) -> bool:
        if code in ("ABS_HAT0X", "ABS_HAT0Y"):
            return value == 0
        return self.deadzone_low <= value <= self.deadzone_high

    def poll_action(self):
        if self.device is None:
            return None

        ready, _, _ = select.select([self.device.fd], [], [], 0)
        if not ready:
            return None

        for event in self.device.read():
            # -------------------------
            # Botões
            # -------------------------
            if event.type == ecodes.EV_KEY and event.value == 1:
                code = ecodes.bytype[ecodes.EV_KEY].get(event.code, str(event.code))

                if code == "BTN_SOUTH":   # X
                    return "select"

                if code == "BTN_EAST":    # O
                    return "back"

                if code == "BTN_START":   # Options
                    return "send"

                if code == "BTN_SELECT":  # Share
                    return "receive"

            # -------------------------
            # Eixos / D-pad / Analógicos
            # -------------------------
            if event.type == ecodes.EV_ABS:
                code = ecodes.bytype[ecodes.EV_ABS].get(event.code, str(event.code))

                if code not in self.last_axis_state:
                    continue

                value = event.value
                prev = self.last_axis_state[code]
                self.last_axis_state[code] = value

                # Se voltou ao neutro, não dispara ação
                if self._neutral_state(code, value):
                    continue

                direction = self._axis_direction(code, value)
                if direction is None:
                    continue

                # D-pad pode repetir normalmente com delay
                if code in ("ABS_HAT0X", "ABS_HAT0Y"):
                    if self._can_navigate():
                        return direction
                    continue

                # Analógico só dispara se:
                # 1) saiu do neutro e cruzou limiar
                # 2) ou repetiu com delay
                prev_neutral = self._neutral_state(code, prev)
                if prev_neutral:
                    if self._can_navigate():
                        return direction
                else:
                    if self._can_navigate():
                        return direction

        return None


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        for path, name in list_gamepads():
            print(f"{path} - {name}")
    else:
        gp = GamepadReader()
        print(gp.name if gp.name else "Nenhum controle encontrado")
