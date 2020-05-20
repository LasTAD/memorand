import PySimpleGUI as sg
from memorand import MemeMan as mg, vk, db_conn as db, util
from datetime import datetime
import time

def main():
    auth = False
    group_id = None
    meme = mg.create_post_meme()
    image_elem = sg.Image(data=mg.get_thumbnail(meme), key="image")
    sg.theme('DarkBlue1')
    col_priv = [[
        sg.Button('Post meme'),
        sg.Button('Prepare meme'),
        sg.Button('Settings')]
    ]
    col_open = [[
        sg.Button('Create meme'),
        sg.Button('Save meme'),
        sg.Button('Authorization')
    ]]
    main_layout = [
        [sg.Button('Create meme'),
         sg.Button('Save meme'),
         sg.Button('Authorization'),
         sg.Column(col_priv, visible=auth, key='HIDE')
         ],
        [sg.Text('Choose meme type'),
         sg.Radio('Post meme', 'MEME', True, key='post'),
         sg.Radio('Demot', 'MEME', key='demot'),
         sg.Radio('Panel', 'MEME', key='panel')
         ],
        [image_elem],
        [sg.Button('Exit')]
    ]
    window = sg.Window('Memorand', main_layout, resizable=True, icon='Resources/278.png')
    settings_active = False
    prep_active = False
    win3_active = False
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            db.conn.close()
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
            if filename:
                mg.save_meme(meme, filename)
        if event == 'Post meme':
            vk.load_meme(mg.prep_for_vk(meme), db.get_phrase(), int(group_id) * (-1), session)
            print('Meme posted' + '\n')
        if event == 'Settings' and not settings_active:
            settings_active = True
            window.Hide()
            groups = vk.get_user_admin_groups(session)
            settings_layout = [
                [sg.Text('Choose group to post your meme:')],
                [sg.Listbox(list(groups.keys()), size=(40, 10), key='GROUP')],
                [sg.Button('OK'), sg.Button('Cancel')]
            ]
            settings_win = sg.Window('Settings', settings_layout)
            while True:
                ev2, vals2 = settings_win.Read()
                if ev2 == 'OK':
                    group_id = groups[vals2['GROUP'][0]]
                    settings_win.close()
                    settings_active = False
                    window.UnHide()
                    break
                if ev2 == 'Cancel':
                    settings_win.close()
                    settings_active = False
                    window.UnHide()
                    break
        if event == 'Prepare meme' and not prep_active:
            window.Hide()
            settings_layout = [
                [sg.Text('Choose time to post your meme:')],
                [sg.InputText('DD', size=(3, 1)), sg.InputText('MM', size=(3, 1)), sg.InputText('YYYY', size=(5, 1))],
                [sg.InputText('HH', size=(3, 1)), sg.Text(':'), sg.InputText('MM', size=(3, 1)),],
                [sg.Button('OK'), sg.Button('Cancel')]
            ]
            prep_win = sg.Window('Settings', settings_layout)
            while True:
                ev_p, vals_p = prep_win.Read()
                if ev_p == 'OK':
                    time_tuple = (int(vals_p[2]), int(vals_p[1]), int(vals_p[0]), int(vals_p[3]), int(vals_p[4]), 0, 0, 0, 0)
                    timestamp = time.mktime(time_tuple)
                    vk.load_meme_postpone(mg.prep_for_vk(meme), db.get_phrase(), int(group_id) * (-1), session, timestamp)
                    prep_win.close()
                    prep_active = False
                    window.UnHide()
                    break
                if ev_p == 'Cancel':
                    prep_win.close()
                    prep_active = False
                    window.UnHide()
                    break
            print('Meme posted' + '\n')
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
                    auth = True
                    window.FindElement('HIDE').Update(visible=auth)
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
