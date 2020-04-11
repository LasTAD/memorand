import os
from PIL import Image, ImageOps
from memorand import MemeMan as mm, db_conn as db

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

def sharp_scale(img, width, height):
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

if __name__ == '__main__':
    in_img1 = Image.open(os.path.join('memorand', 'Resources', db.get_img()))
    in_img2 = Image.open(os.path.join('memorand', 'Resources', db.get_img()))
    img = make_panel_meme(in_img1, in_img2)
    img.save('meme.png')