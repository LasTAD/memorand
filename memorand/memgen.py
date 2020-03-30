import PySimpleGUI as sg
from memorand import MemeMan as mg, vk


def main():
    meme = mg.create_meme()
    image_elem = sg.Image(data=mg.get_thumbnail(meme), key="image")

    sg.theme('DarkBlue1')
    layout = [
        [sg.Button('Create meme'), sg.Button('Save meme'), sg.Button('Exit')],
        [image_elem]
    ]
    window = sg.Window('memgen v0.1', layout, resizable=True)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            print('Goodbye')
            break
        if event == 'Create meme':
            meme = mg.create_meme()
            image_elem.update(data=mg.get_thumbnail(meme))
            window.Refresh()

        if event == 'Save meme':
            # mg.save_meme(meme)
            vk.load_meme(mg.prep_for_vk(meme), 'New era is coming!', -31927652)
            print('Meme saved' + '\n')
    pass


if __name__ == '__main__':
    main()
