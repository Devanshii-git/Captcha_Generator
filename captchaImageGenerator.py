from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random


def generate_captcha_text(length=6):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choices(chars, k=length))


def apply_wave_effect(image, frequency=5, amplitude=3):
    width, height = image.size
    pixels = np.array(image)
    new_pixels = np.zeros_like(pixels)

    for y in range(height):
        shift = int(amplitude * np.sin(2 * np.pi * frequency * y / height))
        new_pixels[y] = np.roll(pixels[y], shift, axis=0)

    return Image.fromarray(new_pixels)


def draw_random_lines(draw, width, height, num_lines=5):
    for _ in range(num_lines):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill="gray", width=random.randint(1, 2))


def draw_random_dots(draw, width, height, num_dots=50):
    for _ in range(num_dots):
        x, y = random.randint(0, width), random.randint(0, height)
        draw.point((x, y), fill="black")


def draw_distorted_text(text, font_size=50, text_color="black", padding=20):
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    total_width = sum(font.getbbox(char)[2] for char in text) + (len(text) - 1) * 15
    total_height = max(font.getbbox(char)[3] for char in text) + padding * 2

    image = Image.new("RGBA", (total_width + padding * 2, total_height), (200, 200, 255, 255))
    draw = ImageDraw.Draw(image)

    x_offset = padding
    for char in text:
        char_width, char_height = font.getbbox(char)[2:]
        y_offset = random.randint(5, 15)
        angle = random.randint(-10, 10)

        char_img = Image.new("RGBA", (char_width, char_height), (0, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((0, 0), char, fill=text_color, font=font)

        char_img = char_img.rotate(angle, expand=True)

        if image.mode != "RGBA":
            image = image.convert("RGBA")

        image.paste(char_img, (x_offset, padding + y_offset), char_img)
        x_offset += char_width + random.randint(10, 15)

    return image


def generate_captcha():
    text = generate_captcha_text()
    image = draw_distorted_text(text, font_size=50, padding=20)

    draw = ImageDraw.Draw(image)
    draw_random_lines(draw, image.width, image.height, num_lines=5)
    draw_random_dots(draw, image.width, image.height, num_dots=50)

    captcha_image = apply_wave_effect(image)
    captcha_image.convert("RGB").save("captcha.png")

    with open("captcha_text.txt", "w") as f:
        f.write(text)

    return text
