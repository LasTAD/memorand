import vk_api
from memorand import vk, db_conn as db
import hashlib as hl
from datetime import datetime
import PySimpleGUI as sg

now = datetime.now()
print = sg.Print


def get_post_text(session, group_name):
    print(now.strftime("%d-%m-%Y %H:%M:%S") + ': Выгрузка постов из группы ' + group_name)
    tools = vk_api.VkTools(session)
    group_id = vk.get_admin_group(group_name, session)
    print(now.strftime("%d-%m-%Y %H:%M:%S") + ': Начало загрузки в целевую таблицу')
    posts = tools.get_all_iter('wall.get', 100, {'owner_id': int(group_id) * -1, 'marked_as_ads': 0})
    conn = db.conn
    cursor = conn.cursor()
    print(now.strftime("%d-%m-%Y %H:%M:%S") + ': Очистка промежуточных таблиц')
    cursor.execute('truncate table stg_phrases cascade;')
    print(now.strftime("%d-%m-%Y %H:%M:%S") + ': Очистка выполнена')
    print(now.strftime("%d-%m-%Y %H:%M:%S") + ': Начинаем выгрузку постов')
    for post in posts:
        if post['text'] != '':
            post_hk = hl.md5(post['text'].encode())
            cursor.execute("insert into stg_phrases (hk, text) values (%s, %s);", (post_hk.hexdigest(), post['text']))
            print(now.strftime("%d-%m-%Y %H:%M:%S") + ': Выгружен ' + str(post['id']))
    print(now.strftime("%d-%m-%Y %H:%M:%S") + ': Загрузка в промежуточные таблицы окончена')
    conn.commit()


def etl_phrases(reload=None):
    conn = db.conn
    cur = conn.cursor()
    print(now.strftime("%d-%m-%Y %H:%M:%S") + ': Начало загрузки в целевую таблицу')
    if reload:
        print(now.strftime("%d-%m-%Y %H:%M:%S") + ': Будет выполнена перезагрузка целевой таблицы!')
        cur.execute('truncate table post_phrases cascade;')
        conn.commit()
        print(now.strftime("%d-%m-%Y %H:%M:%S") + ': Таблица очищена!')
    cur.execute('select distinct * from stg_phrases where hk not in (select hk from post_phrases)')
    phrases = cur.fetchall()
    count = len(phrases)
    print(now.strftime("%d-%m-%Y %H:%M:%S") + ': Количество объектов для загрузки' + str(count))
    for phrase in phrases:
        pal = clean_adul_lng(phrase[1])
        cur.execute('insert into post_phrases(phrase, pal, hk) values (%s, %s, %s);', (phrase[1], pal, phrase[0]))
        print(now.strftime("%d-%m-%Y %H:%M:%S") + ': Загружен ' + phrase[0])
    cur.execute("delete from post_phrases where phrase like '%%www.%%'")
    conn.commit()
    print(now.strftime("%d-%m-%Y %H:%M:%S") + ': Загрузка окончена!')


def clean_adul_lng(str, pal=False):
    ban_list = ['хуй', 'пизд', 'бля', 'елд', 'еб', 'муд', 'ебл', 'пидр', 'пидор', 'вагин', 'охуе', 'хуя', 'ёб']
    str.lower()
    words = list(str.lower().split())
    for word in words:
        for ban_word in ban_list:
            if word.find(ban_word) != -1:
                pal = True
    return pal