import vk_api
import vkauth as vk

# group_id = 31927652, 193569169
# user_id = 153219235
filename = '../newmeme.png'
access_token = '5ef7e83689fe1cba661aa16bb3c9d31643ad5351d98490adee347242cd148fd2912f63d86a564a3518ad9'

# Авторизация
vk_session = vk_api.VkApi(app_id=7382739, token=access_token)
vk_session._auth_token(access_token)




# vk = vk.VKAuth(['photos'], '7382739', '5.52')
# vk.auth()
#
# access_token = vk.get_token()
# user_id = vk.get_user_id()
#
# print(access_token + ' ' + user_id)

def load_meme(file, capture, group_id):
    upload = vk_api.VkUpload(vk_session)  # Для загрузки изображений
    photo_list = upload.photo_wall(file)
    attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)

    # Добавление записи на стену
    vk_session.method("wall.post", {
        'owner_id': group_id,
        'message': capture,
        'attachment': attachment,
    })

def get_admin_group(group_name):
    response = vk_session.method("groups.getById", {
        'group_id': group_name
    })
    if response:
        return response[0]['id']

# def get_user_groups(user) TODO
