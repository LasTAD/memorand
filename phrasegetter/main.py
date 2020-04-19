import PySimpleGUI as sg
from memorand import vk
from phrasegetter import parser as p


def main():
    sg.theme('DarkBlue1')
    layout = [
        [sg.Text('Загрузка фраз в базу')],
        [sg.Button('Authorization')],
        [sg.Text('Link to group'), sg.InputText(size=(15, 1)), sg.Button('Load')],
        [sg.Button('Exit')]
    ]
    window = sg.Window('Memorand', layout, resizable=True)
    win2_active = False
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            print('Goodbye')
            break
        if event == 'Authorization' and not win2_active:
            win2_active = True
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
                    win2_active = False
                    window.UnHide()
                    break
                if ev3 is None or ev3 == 'Exit':
                    win3.close()
                    win2_active = False
                    window.UnHide()
                    break
        if event == 'Load':
            p.get_post_text(session, values[0])
            p.etl_phrases()


if __name__ == '__main__':
    main()
