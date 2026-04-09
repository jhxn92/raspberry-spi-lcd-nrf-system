from RF24 import RF24, RF24_PA_HIGH, RF24_1MBPS

# CE=GPIO17, CSN=CE1 (GPIO7)
radio = RF24(17, 1)
TX_ADDRESS = b"1Node"
RX_ADDRESS = b"2Node"


def init_nrf() -> bool:
    if not radio.begin():
        return False

    radio.setPALevel(RF24_PA_HIGH)
    radio.setDataRate(RF24_1MBPS)
    radio.setChannel(76)
    radio.openWritingPipe(TX_ADDRESS)
    radio.openReadingPipe(1, RX_ADDRESS)
    radio.startListening()
    return True


def send_message(message: str) -> bool:
    payload = message.encode("utf-8")[:32]
    radio.stopListening()
    ok = radio.write(payload)
    radio.startListening()
    return bool(ok)


def receive_message():
    if not radio.available():
        return None

    data = radio.read(32)
    raw = data if isinstance(data, (bytes, bytearray)) else bytes(data)
    return raw.decode("utf-8", errors="ignore").rstrip("\\x00").strip()
