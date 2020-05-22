import vk_api
import PySimpleGUI as sg
import json

vk_file = 'vk_config.v2.json'


def load_meme(file, capture, group_id, session, time=None):
    upload = vk_api.VkUpload(session)  # Для загрузки изображений
    photo_list = upload.photo_wall(file)
    attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)

    if time:
        resp = session.method("wall.post", {
            'owner_id': group_id,
            'message': capture,
            'attachment': attachment,
            'publish_date': time
        })
    else:
        resp = session.method("wall.post", {
            'owner_id': group_id,
            'message': capture,
            'attachment': attachment,
        })

    res = list(resp.keys())
    if res[0] == 'post_id':
        sg.popup_ok('Meme ' + str(resp['post_id']) + ' succesful posted!')
    if res[0] == 'error':
        mesg = str(resp['error']['error_code']) + ': ' + resp['error']['error_msg']
        sg.popup_error(mesg)


def get_user_admin_groups(session):
    with open(vk_file, "r") as read_file:
        data = json.load(read_file)
    user_id = data['kobyzev.n@gmail.com']['token']['app7382739']['scope_270340']['user_id']
    response = session.method("groups.get", {
        'user_id': user_id,
        'filter': 'admin',
        'extended': 1,
        'count': 0
    })
    res = []
    if response:
        l = response['count']
        for x in range(l):
            res.append((response['items'][x]['name'], response['items'][x]['id']))
        r = dict(res)
        return r
    else:
        return 0


def get_group_by_link(session, sh_name):
    resp = session.method("groups.getById", {
        'group_id': sh_name
    })
    return -1 * resp['response']['id']


def vk_auth(email=None, pswd=None):
    vk_session = vk_api.VkApi(
        login=email, password=pswd,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler,
        app_id=7382739,
        scope=270340
    )

    try:
        vk_session.auth()
        sg.popup_ok('Authorization succesful!', auto_close=True)
        return vk_session
    except vk_api.AuthError as error_msg:
        sg.popup_error(error_msg)
        return 0


def auth_handler():
    key = sg.popup_get_text("Enter authentication code", size=(6, 1))
    remember_device = True
    return key, remember_device
