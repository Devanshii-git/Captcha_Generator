from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random


def generate_captcha_text(length=None):
    """Generates a random CAPTCHA text with letters, numbers, and symbols."""
    length = length or random.randint(6, 8)
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$&=+%"
    return "".join(random.choices(chars, k=length))


def apply_wave_effect(image, frequency=5, amplitude=4):
    """Applies a stronger wave distortion effect for added security."""
    width, height = image.size
    pixels = np.array(image)

    for y in range(height):
        shift = int(amplitude * np.sin(2 * np.pi * frequency * y / height))
        pixels[y] = np.roll(pixels[y], shift, axis=0)

    return Image.fromarray(pixels)


def draw_random_lines(draw, width, height, num_lines=6):
    """Draws more random lines for extra distortion."""
    for _ in range(num_lines):
        draw.line(
            [(random.randint(0, width), random.randint(0, height)),
             (random.randint(0, width), random.randint(0, height))],
            fill="gray",
            width=random.randint(1, 3)
        )


def draw_random_dots(draw, width, height, num_dots=40):
    """Adds more random dots to obscure the text slightly."""
    for _ in range(num_dots):
        draw.point((random.randint(0, width), random.randint(0, height)), fill="black")


def draw_distorted_text(text, font_size=50, text_color="black", padding=15):
    """Generates an image with distorted CAPTCHA text."""
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Compute character sizes dynamically
    char_sizes = [font.getbbox(char)[2:4] for char in text]
    total_width = sum(w for w, _ in char_sizes) + (len(text) - 1) * 12 + 2 * padding
    total_height = max(h for _, h in char_sizes) + 2 * padding

    image = Image.new("RGBA", (total_width, total_height), (220, 220, 255, 255))
    draw = ImageDraw.Draw(image)

    x_offset = padding
    for i, char in enumerate(text):
        char_width, char_height = char_sizes[i]
        y_offset = random.randint(-5, 10)  # More vertical randomness
        angle = random.randint(-15, 15)  # Increased rotation for distortion

        char_img = Image.new("RGBA", (char_width, char_height), (0, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((0, 0), char, fill=text_color, font=font)
        char_img = char_img.rotate(angle, expand=True)

        image.paste(char_img, (x_offset, padding + y_offset), char_img)
        x_offset += char_width + random.randint(10, 15)  # More spacing randomness

    return image


def generate_captcha():
    """Generates a CAPTCHA image and saves it."""
    text = generate_captcha_text()
    image = draw_distorted_text(text, font_size=50, padding=15)

    draw = ImageDraw.Draw(image)
    draw_random_lines(draw, image.width, image.height, num_lines=6)  # More lines
    draw_random_dots(draw, image.width, image.height, num_dots=40)  # More dots

    captcha_image = apply_wave_effect(image, frequency=5, amplitude=4)  # Stronger wave effect
    captcha_image.convert("RGB").save("captcha.png")

    with open("captcha_text.txt", "w") as f:
        f.write(text)

    return text
