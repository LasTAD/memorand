import PySimpleGUI as sg
from memorand import MemeMan as mg, vk, db_conn as db


def main():
    global group_id
    group_name = ''
    meme = mg.create_meme()
    image_elem = sg.Image(data=mg.get_thumbnail(meme), key="image")
    sg.theme('DarkBlue1')
    layout = [
        [sg.Button('Create meme'), sg.Button('Post meme'), sg.Button('Exit'), sg.Button('Settings')],
        [image_elem]
    ]
    window = sg.Window('Memorand', layout, resizable=True, icon='Resources/278.png')
    win2_active = False
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            print('Goodbye')
            break
        if event == 'Create meme':
            meme = mg.create_meme()
            image_elem.update(data=mg.get_thumbnail(meme))
            window.Refresh()
        if event == 'Post meme':
            # mg.save_meme(meme)
            vk.load_meme(mg.prep_for_vk(meme), db.get_phrase(), int(group_id)*(-1))
            print('Meme posted' + '\n')
        if event == 'Settings' and not win2_active:
            win2_active = True
            window.Hide()
            layout2 = [[sg.Text('Settings')],
                       [sg.Text('Input your group link-name: '), sg.InputText(group_name)],
                       [sg.Button('Exit'), sg.Button('Save')]]

            win2 = sg.Window('Settings', layout2)
            while True:
                ev2, vals2 = win2.Read()
                if ev2 == 'Save':
                    group_name = vals2[0]
                    group_id = vk.get_admin_group(group_name)
                if ev2 is None or ev2 == 'Exit':
                    win2.close()
                    win2_active = False
                    window.UnHide()
                    break
    pass


if __name__ == '__main__':
    main()
