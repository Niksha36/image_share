from PIL import Image, ImageDraw, ImageTk, ImageFont


#Создаем круглые красивые кнопки
def create_rounded_rectangle_image(width, height, radius, fill_color, text, text_color, font=None, border=None):
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw rounded rectangle
    draw.rounded_rectangle((0, 0, width, height), radius, fill=fill_color)
    if font is None:
        font = ImageFont.truetype("arial.ttf", 16)

    if border is not None:
        draw.rounded_rectangle((0, 0, width, height), radius, outline=border, width=3)
    # Draw text
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2
    draw.text((text_x, text_y), text, fill=text_color, font=font)

    return ImageTk.PhotoImage(image)