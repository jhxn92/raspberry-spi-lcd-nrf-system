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
            if "Motion" in dev.name or "Touchpad" in dev.name:
                continue
            return dev
    return None


class GamepadReader:
    def __init__(self, preferred_name: str = DEFAULT_DEVICE_HINT):
        self.device = find_gamepad(preferred_name)
        self.name = self.device.name if self.device else None

        self.last_nav_time = 0.0
        self.nav_delay = 0.18

        self.analog_threshold_low = 110
        self.analog_threshold_high = 145

    def _can_navigate(self) -> bool:
        now = time.monotonic()
        if now - self.last_nav_time >= self.nav_delay:
            self.last_nav_time = now
            return True
        return False

    def poll_action(self):
        if self.device is None:
            return None

        ready, _, _ = select.select([self.device.fd], [], [], 0)
        if not ready:
            return None

        for event in self.device.read():
            # Botões
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

            # Direcional e analógicos
            if event.type == ecodes.EV_ABS:
                code = ecodes.bytype[ecodes.EV_ABS].get(event.code, str(event.code))

                # D-pad vertical
                if code == "ABS_HAT0Y":
                    if event.value == -1 and self._can_navigate():
                        return "up"
                    if event.value == 1 and self._can_navigate():
                        return "down"

                # D-pad horizontal opcional
                if code == "ABS_HAT0X":
                    if event.value == -1 and self._can_navigate():
                        return "left"
                    if event.value == 1 and self._can_navigate():
                        return "right"

                # Analógico esquerdo vertical
                if code == "ABS_Y":
                    if event.value < self.analog_threshold_low and self._can_navigate():
                        return "up"
                    if event.value > self.analog_threshold_high and self._can_navigate():
                        return "down"

                # Analógico esquerdo horizontal opcional
                if code == "ABS_X":
                    if event.value < self.analog_threshold_low and self._can_navigate():
                        return "left"
                    if event.value > self.analog_threshold_high and self._can_navigate():
                        return "right"

                # Analógico direito vertical opcional
                if code == "ABS_RY":
                    if event.value < self.analog_threshold_low and self._can_navigate():
                        return "up"
                    if event.value > self.analog_threshold_high and self._can_navigate():
                        return "down"

        return None


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        for path, name in list_gamepads():
            print(f"{path} - {name}")
    else:
        gp = GamepadReader()
        print(gp.name if gp.name else "Nenhum controle encontrado")
