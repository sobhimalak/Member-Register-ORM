from Backend import *
import PySimpleGUI as sg


from ORM.Backend import Windows, create_database

create_database()

sg.theme('Black')

layout = [
    [sg.Text("MEMBERSHIP MANAGEMENT", font = header_font, text_color = text_color,
             background_color = '#098E89')],
    [sg.Text("Select an option below to proceed.", font = subtitle_font, text_color = text_color,
             background_color = '#098E89')],
    [sg.Button("ADD MEMBER", key = "-ADD-", size = (20, 1)),
     sg.Button("VIEW MEMBERS", key = "-VIEW-", size = (20, 1)),
     sg.Button("EXIT", key = "-EXIT-", size = (20, 1))]
    ]

window = sg.Window("MEMBERSHIP MANAGEMENT", layout, font = default_font, background_color = '#098E89',
                   text_justification = "center", margins=(60,60),element_justification = "center", no_titlebar = True,grab_anywhere=True)


while True:
    event, values = window.read()
    if event == '-EXIT-' or event == sg.WIN_CLOSED:
        break

    if event == "-ADD-":
        Windows.add_window()

    if event == "-VIEW-":
        Windows.view_window()

    # if event == '-CLEAR-':
    #     clear_Input()

    if event == "-DELETE-":
        Windows.view_window()


window.close()




