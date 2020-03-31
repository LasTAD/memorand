import PySimpleGUI as sg
from memorand import MemeMan as mg, vk, db_conn as db


def main():
    meme = mg.create_meme()
    image_elem = sg.Image(data=mg.get_thumbnail(meme), key="image")

    sg.theme('DarkBlue1')
    layout = [
        [sg.Button('Create meme'), sg.Button('Post meme'), sg.Button('Exit')],
        [image_elem]
    ]
    window = sg.Window('Memorand', layout, resizable=True, icon='Resources/278.png')
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
            vk.load_meme(mg.prep_for_vk(meme), db.get_phrase(), -31927652)
            print('Meme posted' + '\n')
    pass


if __name__ == '__main__':
    main()
