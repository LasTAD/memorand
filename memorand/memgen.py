import PySimpleGUI as sg
from memorand import MemeMan as mg, vk, db_conn as db, util


def main():
    global group_id
    group_name = ''
    meme = mg.create_post_meme()
    image_elem = sg.Image(data=mg.get_thumbnail(meme), key="image")
    sg.theme('DarkBlue1')
    layout = [
        [sg.Button('Create meme'),
         sg.Button('Post meme'),
         sg.Button('Save meme'),
         sg.Button('Settings'),
         sg.Button('Authorization')
         ],
        [sg.Text('Choose meme type'),
         sg.Radio('Post meme', 'MEME', True, key='post'),
         sg.Radio('Demot', 'MEME', key='demot'),
         sg.Radio('Panel', 'MEME', key='panel')
         ],
        [image_elem],
        [sg.Button('Exit')]
    ]
    window = sg.Window('Memorand', layout, resizable=True, icon='Resources/278.png')
    win2_active = False
    win3_active = False
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            print('Goodbye')
            break
        if event == 'Create meme':
            if values['post']:
                meme = mg.create_post_meme()
            if values['demot']:
                meme = mg.create_demot()
            if values['panel']:
                meme = mg.create_panel()
            image_elem.update(data=mg.get_thumbnail(meme))
            window.Refresh()
        if event == 'Save meme':
            filename = sg.popup_get_file('Save meme', save_as=True, file_types=(('PNG', '*.png'),))
            mg.save_meme(meme, filename)
        if event == 'Post meme':
            vk.load_meme(mg.prep_for_vk(meme), db.get_phrase(), int(group_id)*(-1), session)
            print('Meme posted' + '\n')
        if event == 'Settings' and not win2_active:
            win2_active = True
            window.Hide()
            layout2 = [[sg.Text('Settings')],
                       [sg.Text('Input your group link-name: '), sg.InputText(group_name)],
                       [sg.Button('Parser Util')],
                       [sg.Button('Exit'), sg.Button('Save')]]
            win2 = sg.Window('Settings', layout2)
            while True:
                ev2, vals2 = win2.Read()
                if ev2 == 'Save':
                    group_name = vals2[0]
                    group_id = vk.get_admin_group(group_name, session)
                if ev2 == 'Parser Util':
                    win2.Hide()
                    util.main()
                    win2.UnHide()
                if ev2 is None or ev2 == 'Exit':
                    win2.close()
                    win2_active = False
                    window.UnHide()
                    break
        if event == 'Authorization' and not win3_active:
            win3_active = True
            window.Hide()
            layout2 = [[sg.Text('Authorization')],
                       [sg.InputText('Login')],
                       [sg.InputText('Password', password_char='*')],
                       [sg.Button('Exit'), sg.Button('Enter')]]

            win3 = sg.Window('Authorization', layout2)
            while True:
                ev3, vals3 = win3.Read()
                if ev3 == 'Enter':
                    session = vk.vk_auth(vals3[0], vals3[1])
                    win3.close()
                    win3_active = False
                    window.UnHide()
                    break
                if ev3 is None or ev3 == 'Exit':
                    win3.close()
                    win3_active = False
                    window.UnHide()
                    break
    pass


if __name__ == '__main__':
    main()
