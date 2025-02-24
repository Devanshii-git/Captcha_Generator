from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random


def generate_captcha_text(length=None):
    """Generates a random CAPTCHA text with a mix of letters, numbers, and symbols."""
    length = length or random.randint(5, 7)
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$&=+%"
    return "".join(random.choices(chars, k=length))


def apply_wave_effect(image, frequency=3, amplitude=2):
    """Applies a subtle wave distortion effect for security without compromising readability."""
    width, height = image.size
    pixels = np.array(image)

    for y in range(height):
        shift = int(amplitude * np.sin(2 * np.pi * frequency * y / height))
        pixels[y] = np.roll(pixels[y], shift, axis=0)

    return Image.fromarray(pixels)


def draw_random_lines(draw, width, height, num_lines=3):
    """Draws random lines on the CAPTCHA to prevent OCR recognition but not obscure text."""
    for _ in range(num_lines):
        draw.line(
            [(random.randint(0, width), random.randint(0, height)),
             (random.randint(0, width), random.randint(0, height))],
            fill="gray",
            width=random.randint(1, 2)
        )


def draw_random_dots(draw, width, height, num_dots=30):
    """Adds fewer random dots to maintain clarity while increasing complexity."""
    for _ in range(num_dots):
        draw.point((random.randint(0, width), random.randint(0, height)), fill="black")


def draw_distorted_text(text, font_size=48, text_color="black", padding=15):
    """Generates an image with slightly distorted but readable CAPTCHA text."""
    try:
        font = ImageFont.truetype("arial.ttf", font_size)  # Switched to Arial for better clarity
    except IOError:
        font = ImageFont.load_default()

    # Calculate text size dynamically
    char_sizes = [font.getbbox(char)[2:4] for char in text]
    total_width = sum(w for w, _ in char_sizes) + (len(text) - 1) * 10 + 2 * padding
    total_height = max(h for _, h in char_sizes) + 2 * padding

    image = Image.new("RGBA", (total_width, total_height), (220, 220, 255, 255))  # Softer background color
    draw = ImageDraw.Draw(image)

    x_offset = padding
    for i, char in enumerate(text):
        char_width, char_height = char_sizes[i]
        y_offset = random.randint(-3, 5)  # Less vertical displacement for clarity
        angle = random.randint(-8, 8)  # Reduced rotation for better readability

        char_img = Image.new("RGBA", (char_width, char_height), (0, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((0, 0), char, fill=text_color, font=font)
        char_img = char_img.rotate(angle, expand=True)

        image.paste(char_img, (x_offset, padding + y_offset), char_img)
        x_offset += char_width + random.randint(8, 12)  # Optimized spacing

    return image


def generate_captcha():
    """Generates a CAPTCHA image and saves it."""
    text = generate_captcha_text()
    image = draw_distorted_text(text, font_size=48, padding=15)

    draw = ImageDraw.Draw(image)
    draw_random_lines(draw, image.width, image.height, num_lines=3)  # Fewer lines for clarity
    draw_random_dots(draw, image.width, image.height, num_dots=30)  # Fewer dots to improve readability

    captcha_image = apply_wave_effect(image, frequency=3, amplitude=2)  # Less intense wave effect
    captcha_image.convert("RGB").save("captcha.png")

    with open("captcha_text.txt", "w") as f:
        f.write(text)

    return text
