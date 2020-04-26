import os
from PIL import Image
import vk_api
from memorand import vk, db_conn as db
import hashlib as hl
from datetime import datetime
import PySimpleGUI as sg
import shutil as sh


def get_post_text(session, group_name):
    print = sg.Print
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ': Выгрузка постов из группы ' + group_name)
    tools = vk_api.VkTools(session)
    group_id = vk.get_admin_group(group_name, session)
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ': Начало загрузки в целевую таблицу')
    posts = tools.get_all_iter('wall.get', 100, {'owner_id': int(group_id) * -1, 'marked_as_ads': 0})
    conn = db.conn
    cursor = conn.cursor()
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ': Очистка промежуточных таблиц')
    cursor.execute('delete from stg_phrases;')
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ': Очистка выполнена')
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ': Начинаем выгрузку постов')
    for post in posts:
        if post['text'] != '':
            post_hk = hl.md5(post['text'].encode())
            cursor.execute("insert into stg_phrases (hk, text) values (?, ?);", (post_hk.hexdigest(), post['text']))
            print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ': Выгружен ' + str(post['id']))
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ': Загрузка в промежуточные таблицы окончена')
    conn.commit()


def etl_phrases(reload=None):
    print = sg.Print
    conn = db.conn
    cur = conn.cursor()
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ': Начало загрузки в целевую таблицу')
    if reload:
        print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ': Будет выполнена перезагрузка целевой таблицы!')
        cur.execute('delete from stg_phrases;')
        conn.commit()
        print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ': Таблица очищена!')
    cur.execute('select distinct * from stg_phrases where hk not in (select hk from post_phrases)')
    phrases = cur.fetchall()
    count = len(phrases)
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ': Количество объектов для загрузки' + str(count))
    for phrase in phrases:
        pal = clean_adul_lng(phrase[1])
        cur.execute('insert into post_phrases(phrase, pal, hk) values (?, ?, ?);', (phrase[1], pal, phrase[0]))
        print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ': Загружен ' + phrase[0])
    cur.execute("delete from post_phrases where phrase like '%www.%'")
    cur.execute("delete from post_phrases where phrase like '%[c%%'")
    cur.execute("delete from post_phrases where phrase like '%[i%'")
    conn.commit()
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ': Загрузка окончена!')


def clean_adul_lng(str, pal=False):
    ban_list = ['хуй', 'пизд', 'бля', 'елд', 'еб', 'муд', 'ебл', 'пидр', 'пидор', 'вагин', 'охуе', 'хуя', 'ёб']
    str.lower()
    words = list(str.lower().split())
    for word in words:
        for ban_word in ban_list:
            if word.find(ban_word) != -1:
                pal = True
    return pal


def reg_new_res(filepath):
    filename = os.path.basename(filepath)
    conn = db.conn
    cur = conn.cursor()
    hk = hl.md5(Image.open(filepath).tobytes()).hexdigest()
    cur.execute('insert into img_src (img_path, hk)  values (?, ?)', (filename, hk))
    conn.commit()
    sh.copy(filepath, os.path.join(os.path.abspath('.'), 'Resources'))
    return
