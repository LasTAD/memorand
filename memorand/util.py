import PySimpleGUI as sg
from memorand import vk, parser as p


def main(session):
    sg.theme('DarkBlue1')
    layout = [
        [sg.Text('Загрузка фраз в базу')],
        [sg.Text('Link to group'), sg.InputText(size=(30, 1)), sg.Button('Load')],
        [sg.Text('Регистрация картинок в базе')],
        [sg.Text('Path to picture'), sg.InputText(size=(30, 1)), sg.FileBrowse('Choose file'), sg.Button('Register')],
        [sg.Button('Exit')]
    ]
    window = sg.Window('Memorand - Parser util', layout, resizable=True)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            print('Goodbye')
            break

        if event == 'Load':
            p.get_post_text(session, values[0])
            p.etl_phrases()

        if event == 'Register':
            p.reg_new_res(values[1])
    pass
