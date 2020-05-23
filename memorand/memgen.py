import PySimpleGUI as sg
from memorand import MemeMan as mg, vk, db_conn as db, util
import time


def main():
    auth = False
    group_id = None
    meme_type = 0
    meme = mg.create_post_meme()
    image_elem = sg.Image(data=mg.get_thumbnail(meme), key="image")
    sg.theme('DarkBlue1')
    menu_def = [['Post', ['Save meme', 'Make post', 'Make postpone post']],
                ['Settings', ['Authorization', 'Choose admin group', 'Parser util', 'Meme type',
                              ['Post meme', 'Demotivator', '2-panel']], ],
                ['Help', 'About...']]
    main_layout = [
        [sg.Menu(menu_def, )],
        [sg.Button('Create meme'), sg.Button('Make post', visible=auth)],
        [image_elem], ]
    window = sg.Window('Memorand', main_layout, resizable=True)
    while True:
        event, values = window.read()

        if event in (None, 'Exit'):
            db.conn.close()
            print('Goodbye')
            break

        if event == 'Post meme':
            meme_type = 0
        if event == 'Demotivator':
            meme_type = 1
        if event == '2-panel':
            meme_type = 2

        if event == 'Create meme':
            if meme_type == 0:
                meme = mg.create_post_meme()
            if meme_type == 1:
                meme = mg.create_demot()
            if meme_type == 2:
                meme = mg.create_panel()
            image_elem.update(data=mg.get_thumbnail(meme))
            window.Refresh()

        if event == 'Save meme':
            filename = sg.popup_get_file('Save meme', save_as=True, file_types=(('PNG', '*.png'),))
            if filename:
                mg.save_meme(meme, filename)

        if event == 'Make post':
            if not auth:
                sg.popup_error('Authorization needed!')
                continue
            if group_id is None:
                sg.popup_error('Choose group to post!')
                continue
            vk.load_meme(mg.prep_for_vk(meme), db.get_phrase(), int(group_id) * (-1), session)
            print('Meme posted' + '\n')

        if event == 'Choose admin group':
            if not auth:
                sg.popup_error('Authorization needed!')
                continue
            group_id = admin_group_window(window, session)

        if event == 'Make postpone post':
            if not auth:
                sg.popup_error('Authorization needed!')
                continue
            if group_id is None:
                sg.popup_error('Choose group to post!')
                continue
            postpone_post(window, session, meme, group_id)

        if event == 'Authorization':
            session = authorization(window)
            if session == 0:
                continue
            group_id = admin_group_window(window, session)
            auth = True

        if event == 'Parser util':
            if not auth:
                sg.popup_error('Authorization needed!')
                continue
            window.Hide()
            util.main(session)
            window.UnHide()

        if event == 'About...':
            sg.popup('About Memorand', 'Version 1.5', 'Cyber-era is already here!\nAuthor: Kobyzev N. & Nikolaeva V.')
    pass


def admin_group_window(window, session):
    window.Hide()
    groups = vk.get_user_admin_groups(session)
    layout = [
        [sg.Text('Choose group to post your meme:')],
        [sg.Listbox(list(groups.keys()), size=(40, 10), key='GROUP')],
        [sg.Button('OK'), sg.Button('Cancel')]
    ]
    win = sg.Window('Admin groups', layout)
    while True:
        events, values = win.Read()
        if events == 'OK':
            group_id = groups[values['GROUP'][0]]
            win.close()
            window.UnHide()
            break
        if events == 'Cancel':
            win.close()
            window.UnHide()
            break
    return group_id


def authorization(window):
    window.Hide()
    layout = [[sg.Text('Authorization')],
              [sg.InputText('Login')],
              [sg.InputText('Password', password_char='*')],
              [sg.Button('Exit'), sg.Button('Enter')]]
    win = sg.Window('Authorization', layout)
    while True:
        events, values = win.Read()
        if events == 'Enter':
            session = vk.vk_auth(values[0], values[1])
            if session != 0:
                auth = True
                window.FindElement('Make post').Update(visible=auth)
            win.close()
            window.UnHide()
            break
        if events is None or events == 'Exit':
            win.close()
            session = 0
            window.UnHide()
            break
    return session


def postpone_post(window, session, meme, group_id):
    window.Hide()
    layout = [
        [sg.Text('Choose time to post your meme:')],
        [sg.InputText('DD', size=(3, 1)), sg.InputText('MM', size=(3, 1)), sg.InputText('YYYY', size=(5, 1))],
        [sg.InputText('HH', size=(3, 1)), sg.Text(':'), sg.InputText('MM', size=(3, 1)), ],
        [sg.Button('OK'), sg.Button('Cancel')]
    ]
    win = sg.Window('Postpone post', layout)
    while True:
        events, values = win.Read()
        if events == 'OK':
            time_tuple = (
                int(values[2]), int(values[1]), int(values[0]), int(values[3]), int(values[4]), 0, 0, 0, 0)
            timestamp = time.mktime(time_tuple)
            vk.load_meme(mg.prep_for_vk(meme), db.get_phrase(), int(group_id) * (-1), session, timestamp)
            win.close()
            window.UnHide()
            break
        if events == 'Cancel':
            win.close()
            window.UnHide()
            break
    print('Meme posted' + '\n')


if __name__ == '__main__':
    main()
