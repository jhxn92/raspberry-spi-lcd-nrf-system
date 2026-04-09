import sys
from evdev import InputDevice, list_devices, ecodes

DEFAULT_DEVICE_HINT = "Wireless Controller"

def list_gamepads():
    devices = []
    for path in list_devices():
        dev = InputDevice(path)
        devices.append((path, dev.name))
    return devices

def find_gamepad(preferred_name=DEFAULT_DEVICE_HINT):
    for path in list_devices():
        dev = InputDevice(path)
        if preferred_name.lower() in dev.name.lower():
            return dev
    return None

class GamepadReader:
    def __init__(self, preferred_name=DEFAULT_DEVICE_HINT):
        self.device = find_gamepad(preferred_name)
        self.name = self.device.name if self.device else None

    def poll_action(self):
        if self.device is None:
            return None
        for event in self.device.read():
            if event.type == ecodes.EV_KEY and event.value == 1:
                code = ecodes.bytype[ecodes.EV_KEY].get(event.code, str(event.code))
                if code == "BTN_SOUTH":
                    return "select"
                if code == "BTN_EAST":
                    return "back"
                if code == "BTN_START":
                    return "send"
                if code == "BTN_SELECT":
                    return "receive"
            if event.type == ecodes.EV_ABS:
                code = ecodes.bytype[ecodes.EV_ABS].get(event.code, str(event.code))
                if code == "ABS_HAT0Y":
                    if event.value == -1:
                        return "up"
                    if event.value == 1:
                        return "down"
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        for path, name in list_gamepads():
            print(f"{path} - {name}")
    else:
        gp = GamepadReader()
        print(gp.name if gp.name else "Nenhum controle encontrado")
