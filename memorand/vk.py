import vk_api
from memorand import vkauth as vk
import json


def load_meme(file, capture, group_id, session):
    upload = vk_api.VkUpload(session)  # Для загрузки изображений
    photo_list = upload.photo_wall(file)
    attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)

    # Добавление записи на стену
    session.method("wall.post", {
        'owner_id': group_id,
        'message': capture,
        'attachment': attachment,
    })


def get_admin_group(group_name, session):
    response = session.method("groups.getById", {
        'group_id': group_name
    })
    if response:
        return response[0]['id']


# def get_user_groups(user) TODO

def vk_auth(email, pswd):
    auth = vk.VKAuth(['photos', 'wall', 'groups'], '7382739', '5.52')
    auth.auth(email, pswd)

    access_token = auth.get_token()
    vk_session = vk_api.VkApi(app_id=7382739, token=access_token, config_filename='vk_config.v2.json')
    vk_session._auth_token(access_token)
    return vk_session

def vk_auth_token(token):
    vk_session = vk_api.VkApi(app_id=7382739, token=token)
    vk_session._auth_token(token)
    return vk_session
