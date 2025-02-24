from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random


def generate_captcha_text(length=None):
    length = length or random.randint(5, 7)
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$&=+%"
    return "".join(random.choices(chars, k=length))


def apply_wave_effect(image, frequency=5, amplitude=3):
    width, height = image.size
    pixels = np.array(image)

    for y in range(height):
        shift = int(amplitude * np.sin(2 * np.pi * frequency * y / height))
        pixels[y] = np.roll(pixels[y], shift, axis=0)

    return Image.fromarray(pixels)


def draw_random_lines(draw, width, height, num_lines=5):
    for _ in range(num_lines):
        draw.line(
            [(random.randint(0, width), random.randint(0, height)),
             (random.randint(0, width), random.randint(0, height))],
            fill="gray",
            width=random.randint(1, 2)
        )


def draw_random_dots(draw, width, height, num_dots=50):
    for _ in range(num_dots):
        draw.point((random.randint(0, width), random.randint(0, height)), fill="black")


def draw_distorted_text(text, font_size=50, text_color="black", padding=20):
    try:
        font = ImageFont.truetype("times.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    char_sizes = [font.getbbox(char)[2:4] for char in text]
    total_width = sum(w for w, _ in char_sizes) + (len(text) - 1) * 15
    total_height = max(h for _, h in char_sizes) + padding * 2

    image = Image.new("RGBA", (total_width + padding * 2, total_height), (200, 200, 255, 255))
    draw = ImageDraw.Draw(image)

    x_offset = padding
    for i, char in enumerate(text):
        char_width, char_height = char_sizes[i]
        y_offset = random.randint(5, 15)
        angle = random.randint(-10, 10)

        char_img = Image.new("RGBA", (char_width, char_height), (0, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((0, 0), char, fill=text_color, font=font)
        char_img = char_img.rotate(angle, expand=True)

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

