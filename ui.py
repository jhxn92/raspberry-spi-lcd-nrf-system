from PIL import Image, ImageDraw, ImageFont

WIDTH = 128
HEIGHT = 160
HEADER_H = 20
font = ImageFont.load_default()

def create_canvas():
    image = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    return image, draw

def header(draw, title):
    draw.rectangle((0, 0, WIDTH, HEADER_H), fill=(20, 20, 20))
    draw.text((5, 5), title, fill=(255, 255, 255), font=font)

def menu(draw, options, selected):
    y0 = 34
    for i, opt in enumerate(options):
        y = y0 + i * 22
        if i == selected:
            draw.rounded_rectangle((6, y - 2, WIDTH - 6, y + 14), radius=5, fill=(40, 40, 40))
            color = (255, 255, 255)
        else:
            color = (140, 140, 140)
        draw.text((12, y), opt, fill=color, font=font)

def footer(draw, text):
    draw.text((6, HEIGHT - 12), text, fill=(100, 100, 100), font=font)

def body_text(draw, text, y=36, color=(255, 255, 255)):
    draw.text((8, y), text, fill=color, font=font)
