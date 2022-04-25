import PySimpleGUI as sg
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO


def update_img(orig, blur, contrast, emboss, contour, flipx, flipy, water):
    global img

    img = orig.filter(ImageFilter.GaussianBlur(blur))
    img = img.filter(ImageFilter.UnsharpMask(contrast))
    if emboss:
        img = img.filter(ImageFilter.EMBOSS())
    if contour:
        img = img.filter(ImageFilter.CONTOUR())
    if flipx:
        img = ImageOps.flip(img)
    if flipy:
        img = ImageOps.mirror(img)

    watermark = Image.open("logo.png")
    watermark_adj = watermark.resize((int(orig_img.width * .4), int(orig_img.height * .15)))
    if water == 'Watermark Bottom Left':
        img.paste(im=watermark_adj, box=(10, orig_img.height - watermark_adj.height - 10), mask=watermark_adj)
    elif water == 'Watermark Bottom Right':
        img.paste(im=watermark_adj, box=(orig_img.width - watermark_adj.width - 10, orig_img.height - watermark_adj.height - 10), mask=watermark_adj)
    elif water == 'Watermark Top Left':
        img.paste(im=watermark_adj, box=(10, watermark_adj.height - 10), mask=watermark_adj)
    elif water == 'Watermark Top Right':
        img.paste(im=watermark_adj, box=(orig_img.width - watermark_adj.width - 10, watermark_adj.height - 10), mask=watermark_adj)

    bio = BytesIO()
    img.save(bio, format='png')
    window['IMG'].update(data=bio.getvalue())


img_path = sg.popup_get_file('Open', no_window=True, file_types=(('PNG Files', '*.png'), ('GIF Files', '*.gif')))

left_col = sg.Column([
    [sg.Frame(title="Blur", layout=[[sg.Slider((0, 10), orientation='h', key='BLUR')]])],
    [sg.Frame(title="Contrast", layout=[[sg.Slider((0, 10), orientation='h', key='CONTRAST')]])],
    [sg.Checkbox("Emboss", key='EMB'), sg.Checkbox("Contour", key='CONTOUR')],
    [sg.Checkbox("Flip x    ", key='FLIPX'), sg.Checkbox("Flip y", key='FLIPY')],
    [sg.Combo(['No Watermark',
               'Watermark Bottom Left',
               'Watermark Bottom Right',
               'Watermark Top Left',
               'Watermark Top Right'],
              default_value='No Watermark', key='WATER')],
    [sg.Button("Save Image", key='SAVE')],
])
right_col = sg.Column([
    [sg.Image(img_path, key='IMG')],
])
layout = [[left_col, right_col]]

orig_img = Image.open(img_path)

window = sg.Window('Image Editor', layout)
while True:
    event, values = window.read(timeout=50)
    if event == sg.WIN_CLOSED:
        break
    update_img(orig_img,
               values['BLUR'],
               values['CONTRAST'],
               values['EMB'],
               values['CONTOUR'],
               values['FLIPX'],
               values['FLIPY'],
               values['WATER'],)
    if event == 'SAVE':
        save_path = f'{sg.popup_get_file("Save As", save_as=True, no_window=True)}.png'
        img.save(save_path, 'PNG')

window.close()
