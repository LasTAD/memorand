from PIL import ImageFont, ImageDraw, Image
import io
from memorand import k_mean, db_conn as db
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("../memorand")
    return os.path.join(base_path, relative_path)


def scale_image(img,
                width=None,
                height=None
                ):
    w, h = img.size

    if width and height:
        max_size = (width, height)
    elif width:
        max_size = (width, h)
    elif height:
        max_size = (w, height)
    else:
        raise RuntimeError('Width or height required!')
    img.thumbnail(max_size, Image.ANTIALIAS)
    return img


def get_thumbnail(img):
    im = img
    im_bytes = io.BytesIO()
    im.save(im_bytes, format="GIF")
    return im_bytes.getvalue()


def font_change(txt: str, img: Image, div: float):
    fontsize = 1
    img_fraction = 0.9
    font = ImageFont.truetype('Resources/Lobster.ttf', fontsize)
    while font.getsize(txt)[0] / div < img_fraction * img.size[0]:
        fontsize += 1
        font = ImageFont.truetype('Resources/Lobster.ttf', fontsize)
    fontsize -= 1
    return fontsize


def put_text_pil(img: Image, txt: str):
    maxfontsize = 50
    w_i, h_i = img.size
    if w_i > 500:
        scale_image(img, width=500)
    if h_i > 500:
        scale_image(img, height=500)
    w_i, h_i = img.size
    fontsize = font_change(txt, img, 1.0)
    if fontsize <= 18:
        txt_len = len(txt)
        mid_space = txt.find(' ', len(txt) // 2)
        txt_end = txt[mid_space + 1:]
        txt_end = txt_end.center(mid_space)
        txt_start = txt[:mid_space]
        txt = txt_start + "\n" + txt_end
        txt = txt.strip()
        fontsize = font_change(txt, img, txt_len / len(txt_start))
    if fontsize > maxfontsize:
        fontsize = maxfontsize
    print('final font size: ', fontsize)
    font = ImageFont.truetype('Resources/Lobster.ttf', fontsize)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(txt, font=font)

    y_pos = h_i - h - h_i * 0.05
    x_pos = (w_i - w) / 2
    draw = ImageDraw.Draw(img)
    text_size = (x_pos, y_pos, x_pos+w, y_pos + h)
    print(text_size)
    font_col = k_mean.pick_color(img, text_size)

    offset = 2
    shadowColor = 'black'

    for off in range(offset):
        draw.text((x_pos - off, y_pos), txt, font=font, fill=shadowColor)
        draw.text((x_pos + off, y_pos), txt, font=font, fill=shadowColor)
        draw.text((x_pos, y_pos + off), txt, font=font, fill=shadowColor)
        draw.text((x_pos, y_pos - off), txt, font=font, fill=shadowColor)
        draw.text((x_pos - off, y_pos + off), txt, font=font, fill=shadowColor)
        draw.text((x_pos + off, y_pos + off), txt, font=font, fill=shadowColor)
        draw.text((x_pos - off, y_pos - off), txt, font=font, fill=shadowColor)
        draw.text((x_pos + off, y_pos - off), txt, font=font, fill=shadowColor)
    draw.text((x_pos, y_pos), txt, fill=font_col, font=font)
    return img


def create_meme():
    img = Image.open(resource_path(db.get_img()))
    img = put_text_pil(img, db.get_phrase())
    return img


def save_meme(img):
    filename = os.path.abspath(os.curdir) + "/newmeme.png"
    img.save(filename)
    return filename

def prep_for_vk(img):
    b = io.BytesIO()
    img.save(b, "JPEG")
    b.seek(0)
    return b