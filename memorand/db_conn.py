import sqlite3
import os

conn = sqlite3.connect(os.path.join(os.path.abspath('.'), 'Resources', 'postdb.db'))

def get_phrase():
    cursor = conn.cursor()
    cursor.execute('select phrase from post_phrases order by random() --where pal = false order by random();')
    phrase = cursor.fetchone()[0]
    phrase = phrase.strip()
    print(phrase)
    return phrase


def get_img():
    cursor = conn.cursor()
    cursor.execute("select img_path from img_src order by random()")
    img_path = cursor.fetchone()[0]
    print(img_path)
    return img_path
