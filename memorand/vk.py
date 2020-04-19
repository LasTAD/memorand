import vk_api
import PySimpleGUI as sg


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
    # auth = vk.VKAuth(['photos', 'wall', 'groups'], '7382739', '5.92')
    # auth.auth(email, pswd)
    #
    # access_token = auth.get_token()
    # vk_session = vk_api.VkApi(app_id=7382739, token=access_token, config_filename='vk_config.v2.json')
    # vk_session._auth_token(access_token)

    vk_session = vk_api.VkApi(
        login=email, password=pswd,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler,
        app_id=7382739,
        scope=270340
    )

    try:
        vk_session.auth()
        return vk_session
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return


def vk_auth_token(token):
    vk_session = vk_api.VkApi(app_id=7382739, token=token)
    vk_session._auth_token(token)
    return vk_session


def auth_handler():
    key = sg.popup_get_text("Enter authentication code", size=(6, 1))
    remember_device = True
    return key, remember_device
