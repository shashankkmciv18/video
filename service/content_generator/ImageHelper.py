from PIL import Image, ImageDraw, ImageFont
import os


def overlay_text_on_image_vertical(quote):
    from textwrap import wrap

    resources_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources"))
    background_image_path = os.path.join(resources_dir, 'background.jpg')

    # Open the image
    img = Image.open(background_image_path)
    img = img.resize((1080, 1920))  # Resize to vertical aspect ratio
    draw = ImageDraw.Draw(img)

    # Load a TTF font (system font or download a font)
    font_path = os.path.join(resources_dir, "arial.ttf")  # Change if necessary or download a font
    font_size = 100
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text size and wrap text
    img_width, img_height = img.size
    max_width = img_width * 0.8  # Allow some padding
    wrapped_text = quote
    while True:
        lines = wrap(wrapped_text, width=40)  # Adjust width for wrapping
        line_widths = [draw.textlength(line, font=font) for line in lines]
        if all(width <= max_width for width in line_widths):
            break
        font_size -= 2
        font = ImageFont.truetype(font_path, font_size)

    # Calculate total text height
    line_height = draw.textbbox((0, 0), "A", font=font)[3] - draw.textbbox((0, 0), "A", font=font)[1]
    line_spacing = line_height * 0.5  # Dynamic spacing as 50% of line height
    total_text_height = (line_height + line_spacing) * len(lines) - line_spacing

    y = (img_height * 0.75) - (total_text_height / 2)
    shadow_color = "black"
    text_color = "white"

    for line in lines:
        text_width = draw.textlength(line, font=font)
        x = (img_width - text_width) / 2  # Center align each line
        draw.text((x - 2, y - 2), line, font=font, fill=shadow_color)
        draw.text((x + 2, y - 2), line, font=font, fill=shadow_color)
        draw.text((x - 2, y + 2), line, font=font, fill=shadow_color)
        draw.text((x + 2, y + 2), line, font=font, fill=shadow_color)
        draw.text((x, y), line, font=font, fill=text_color)
        y += line_height + line_spacing

    output_image = os.path.join(resources_dir, 'final_background_vertical.jpg')

    img.save(output_image)
