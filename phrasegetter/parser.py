import vk_api
from memorand import vk, db_conn as db
import hashlib as hl


def get_post_text(session, group_name):
    group_id = vk.get_admin_group(group_name, session)
    tools = vk_api.VkTools(session)
    posts = tools.get_all_iter('wall.get', 100, {'owner_id': int(group_id) * -1, 'marked_as_ads': 0})
    conn = db.conn
    cursor = conn.cursor()
    for post in posts:
        post_hk = hl.md5(post['text'].encode())
        cursor.execute("insert into stg_phrases (hk, text) values (%s, %s);", (post_hk.hexdigest(), post['text']))
        print(post['id'])
    conn.commit()


def etl_phrases(reload=None):
    conn = db.conn
    cur = conn.cursor()
    if reload:
        cur.execute('truncate table post_phrases cascade;')
        conn.commit()
    cur.execute('select distinct * from stg_phrases where hk not in (select hk from post_phrases)')
    phrases = cur.fetchall()
    for phrase in phrases:
        pal = clean_adul_lng(phrase[1])
        cur.execute('insert into post_phrases(phrase, pal, hk) values (%s, %s, %s);', (phrase[1], pal, phrase[0]))
        print(phrase[0])
    cur.execute("delete from post_phrases where phrase like '%%www.%%'")
    conn.commit()


def clean_adul_lng(str, pal=False):
    ban_list = ['хуй', 'пизд', 'бля', 'елд', 'еб', 'муд', 'ебл', 'пидр', 'пидор', 'вагин', 'охуе', 'хуя', 'ёб']
    str.lower()
    words = list(str.lower().split())
    for word in words:
        for ban_word in ban_list:
            if word.find(ban_word) != -1:
                pal = True
    return pal