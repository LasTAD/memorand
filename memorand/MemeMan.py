from PIL import ImageFont, ImageDraw, Image, ImageOps
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
    im = image_scale(img, 500)
    im_bytes = io.BytesIO()
    im.save(im_bytes, format="GIF")
    return im_bytes.getvalue()


def font_change(txt: str, w_i, div: float, font_name):
    fontsize = 1
    img_fraction = 0.9
    font = ImageFont.truetype(font_name, fontsize)
    while font.getsize(txt)[0] / div < img_fraction * w_i:
        fontsize += 1
        font = ImageFont.truetype(font_name, fontsize)
    fontsize -= 1
    return fontsize


def make_post_meme(img: Image, txt: str):
    font_name = os.path.join('memorand', 'Resources', 'Lobster.ttf')
    img = image_scale(img, 500)
    w_i, h_i = img.size
    put_font = put_text(img, txt, font_name)
    fontsize, txt = put_font
    font = ImageFont.truetype(os.path.join('memorand', 'Resources', 'Lobster.ttf'), fontsize)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(txt, font=font)

    y_pos = h_i - h - h_i * 0.05
    x_pos = (w_i - w) / 2
    draw = ImageDraw.Draw(img)
    text_size = (x_pos, y_pos, x_pos + w, y_pos + h)
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


# todo
def make_demot(img, txt):
    border = 0.1
    img = image_scale(img, 500)
    w_i, h_i = img.size
    font_name = os.path.join('memorand', 'Resources', 'Times New Roman.ttf')
    put_font = put_text(img, txt, font_name)
    fontsize, txt = put_font
    font = ImageFont.truetype(font_name, fontsize)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(txt, font=font)

    bimg = ImageOps.expand(img, border=(int(w_i * 0.01)), fill='black')
    bimg = ImageOps.expand(bimg, border=1, fill='white')
    bimg = ImageOps.expand(bimg, border=(int(w_i * border),
                                         int(w_i * border),
                                         int(w_i * border),
                                         int(h + 30) if w_i * border < h + 30 else int(w_i * border)),
                           fill='black')
    img = bimg
    w_i, h_i = img.size
    y_pos = h_i - h - 20
    x_pos = (w_i - w) / 2
    draw = ImageDraw.Draw(img)
    text_size = (x_pos, y_pos, x_pos + w, y_pos + h)
    print(text_size)
    draw.text((x_pos, y_pos), txt, fill='white', font=font)
    return img


def image_scale(img, size):
    w_i, h_i = img.size
    if w_i > size:
        img = scale_image(img, width=500)
    if h_i > size:
        img = scale_image(img, height=500)
    return img


def put_text(img, txt, font_name):
    maxfontsize = 50
    w_i, h_i = img.size
    fontsize = font_change(txt, w_i, 1.0, font_name)
    if fontsize <= 18:
        txt_len = len(txt)
        mid_space = txt.find(' ', len(txt) // 2)
        txt_end = txt[mid_space + 1:]
        txt_end = txt_end.center(mid_space)
        txt_start = txt[:mid_space]
        txt = txt_start + "\n" + txt_end
        txt = txt.strip()
        fontsize = font_change(txt, w_i, txt_len / len(txt_start), font_name)
    if fontsize > maxfontsize:
        fontsize = maxfontsize
    return fontsize, txt


def make_panel_meme(img1, img2):
    img1 = sharp_scale(img1, 500)
    w_1, h_1 = img1.size
    img2 = sharp_scale(img2, 500)
    w_2, h_2 = img2.size
    print(w_1, h_1, w_2, h_2)
    img = Image.new('RGB', (w_1, h_1 + h_2))
    img.paste(img1, (0, 0))
    img.paste(img2, (0, h_1))
    return img

def sharp_scale(img, width = None, height = None):
    w, h = img.size
    if width:
        ratio = (width / float(w))
        height = int((float(h) * float(ratio)))
        img = img.resize((width, height), Image.ANTIALIAS)
    elif height:
        ratio = (height / float(h))
        width = int((float(w) * float(ratio)))
        img = img.resize((width, height), Image.ANTIALIAS)
    return img


def create_panel():
    img1 = create_post_meme()
    img2 = create_post_meme()
    return make_panel_meme(img1, img2)



def create_post_meme():
    img = Image.open(os.path.join('memorand', 'Resources', db.get_img()))
    return make_post_meme(img, db.get_phrase())



def create_demot():
    img = Image.open(os.path.join('memorand', 'Resources', db.get_img()))
    return make_demot(img, db.get_phrase())


def save_meme(img, filename):
    img.save(filename)
    return filename


def prep_for_vk(img):
    b = io.BytesIO()
    img.save(b, "PNG")
    b.seek(0)
    return b
