from RF24 import RF24, RF24_PA_HIGH, RF24_1MBPS

# CE=GPIO17, CSN=CE1 (GPIO7)
radio = RF24(17, 1)

TX_ADDRESS = b"1Node"
RX_ADDRESS = b"2Node"


def init_nrf() -> bool:
    try:
        if not radio.begin():
            print("NRF: radio.begin() falhou")
            return False

        radio.setPALevel(RF24_PA_HIGH)
        radio.setDataRate(RF24_1MBPS)
        radio.setChannel(76)

        # Menos tempo preso em tentativa de envio
        radio.setRetries(3, 5)

        # Para teste, desligamos ACK automático.
        # Isso evita travas se o outro rádio ainda não estiver pronto.
        radio.setAutoAck(False)

        radio.openWritingPipe(TX_ADDRESS)
        radio.openReadingPipe(1, RX_ADDRESS)
        radio.startListening()

        print("NRF: inicializado com sucesso")
        return True

    except Exception as e:
        print(f"NRF: erro na inicializacao: {e}")
        return False


def send_message(message: str) -> bool:
    try:
        payload = message.encode("utf-8")[:32]

        radio.stopListening()
        ok = radio.write(payload)
        radio.startListening()

        print(f"NRF: envio={'OK' if ok else 'FALHA'} mensagem={message!r}")
        return bool(ok)

    except Exception as e:
        print(f"NRF: erro no envio: {e}")
        try:
            radio.startListening()
        except Exception:
            pass
        return False


def receive_message():
    try:
        if not radio.available():
            return None

        data = radio.read(32)
        raw = data if isinstance(data, (bytes, bytearray)) else bytes(data)
        text = raw.decode("utf-8", errors="ignore").rstrip("\x00").strip()

        if text:
            print(f"NRF: recebido={text!r}")

        return text if text else None

    except Exception as e:
        print(f"NRF: erro na recepcao: {e}")
        return None
