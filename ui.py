from PIL import Image, ImageDraw, ImageFont

WIDTH = 160
HEIGHT = 128

HEADER_H = 18
FOOTER_H = 12

FONT = ImageFont.load_default()


def create_canvas():
    image = Image.new("RGB", (WIDTH, HEIGHT), (8, 8, 10))
    draw = ImageDraw.Draw(image)
    return image, draw


def create_offscreen():
    image = Image.new("RGB", (WIDTH, HEIGHT), (8, 8, 10))
    draw = ImageDraw.Draw(image)
    return image, draw


def _safe_rounded_rect(draw, box, radius, fill=None, outline=None):
    try:
        draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline)
    except Exception:
        draw.rectangle(box, fill=fill, outline=outline)


def header(draw, title: str) -> None:
    _safe_rounded_rect(
        draw,
        (0, 0, WIDTH - 1, HEADER_H),
        radius=0,
        fill=(18, 18, 22),
    )
    draw.line((0, HEADER_H, WIDTH, HEADER_H), fill=(35, 35, 42), width=1)
    draw.text((6, 4), title[:22], fill=(245, 245, 245), font=FONT)


def footer(draw, text: str) -> None:
    y = HEIGHT - FOOTER_H
    draw.line((0, y - 2, WIDTH, y - 2), fill=(25, 25, 30), width=1)
    draw.text((6, y), text[:26], fill=(120, 120, 128), font=FONT)


def body_text(draw, text: str, y: int = 32, color=(235, 235, 235)) -> None:
    draw.text((8, y), text[:24], fill=color, font=FONT)


def info_label(draw, label: str, value: str, y: int) -> None:
    draw.text((8, y), label[:16], fill=(150, 150, 160), font=FONT)
    draw.text((8, y + 14), value[:22], fill=(240, 240, 240), font=FONT)


def status_pill(draw, x: int, y: int, text: str, ok: bool = True) -> None:
    w = min(max(36, len(text) * 6 + 10), WIDTH - x - 4)
    fill = (18, 70, 52) if ok else (90, 36, 36)
    outline = (38, 130, 92) if ok else (160, 70, 70)

    _safe_rounded_rect(
        draw,
        (x, y, x + w, y + 14),
        radius=6,
        fill=fill,
        outline=outline,
    )
    draw.text((x + 6, y + 3), text[:18], fill=(255, 255, 255), font=FONT)


def card(draw, title: str, lines: list[str], y: int = 28, h: int = 72) -> None:
    _safe_rounded_rect(
        draw,
        (6, y, WIDTH - 6, y + h),
        radius=8,
        fill=(15, 15, 18),
        outline=(35, 35, 42),
    )

    draw.text((12, y + 8), title[:20], fill=(245, 245, 245), font=FONT)

    yy = y + 26
    for line in lines[:3]:
        draw.text((12, yy), line[:22], fill=(185, 185, 190), font=FONT)
        yy += 14


def section_title(draw, text: str, y: int) -> None:
    draw.text((8, y), text[:20], fill=(165, 165, 175), font=FONT)
    draw.line((8, y + 10, WIDTH - 8, y + 10), fill=(28, 28, 34), width=1)


def center_text(draw, text: str, y: int, color=(255, 255, 255)) -> None:
    text = text[:24]
    approx_w = len(text) * 6
    x = max(0, (WIDTH - approx_w) // 2)
    draw.text((x, y), text, fill=color, font=FONT)


def empty_state(draw, title: str, subtitle: str = "") -> None:
    center_text(draw, title, 42, (220, 220, 220))
    if subtitle:
        center_text(draw, subtitle, 62, (120, 120, 128))


def progress_bar(draw, x: int, y: int, w: int, h: int, value: float) -> None:
    value = max(0.0, min(1.0, value))
    _safe_rounded_rect(
        draw,
        (x, y, x + w, y + h),
        radius=4,
        fill=(20, 20, 24),
        outline=(42, 42, 48),
    )
    fill_w = int((w - 2) * value)
    if fill_w > 0:
        _safe_rounded_rect(
            draw,
            (x + 1, y + 1, x + 1 + fill_w, y + h - 1),
            radius=3,
            fill=(220, 220, 220),
        )


def menu(draw, options, selected: int, highlight_y=None) -> None:
    start_y = 30
    step = 22

    if highlight_y is None:
        highlight_y = start_y + selected * step

    _safe_rounded_rect(
        draw,
        (6, highlight_y - 3, WIDTH - 6, highlight_y + 15),
        radius=7,
        fill=(32, 32, 38),
        outline=(56, 56, 66),
    )
    draw.rectangle((9, highlight_y, 11, highlight_y + 11), fill=(255, 255, 255))

    for i, opt in enumerate(options):
        y = start_y + i * step
        color = (255, 255, 255) if i == selected else (135, 135, 145)
        draw.text((16, y), opt[:20], fill=color, font=FONT)
