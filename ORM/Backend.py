import sqlite3
import PySimpleGUI as sg
from ORM import validation

header_font = ("Poppins", 32)
subtitle_font = ("Poppins", 24)
default_font = ("Poppins", 16)
background_color = 'Black'
text_color = '#ffffff'


def create_database():
    conn = sqlite3.connect("OrmDatabase.db")
    query = (""" CREATE TABLE IF NOT EXISTS MEMBERS (
        id_num INTEGER PRIMARY KEY NOT NULL,
        first_name VARCHAR(25) NOT NULL,
        last_name VARCHAR(25) NOT NULL,
        address VARCAHR(50) NOT NULL,
        post_number INTEGER NOT NULL,
        subscription TEXT NOT NULL); """)
    conn.execute(query)
    conn.close()


def insert_contact(first_name, last_name, address, post_number, subscription):
    insert_conn = sqlite3.connect("OrmDatabase.db")
    insert_conn.execute(""" INSERT INTO MEMBERS (first_name, last_name, address, post_number,subscription) 
            VALUES (?, ?, ?, ?, ?) """, (first_name, last_name, address, post_number, subscription))
    insert_conn.commit()
    insert_conn.close()


class Windows:
    @staticmethod
    def add_window():
        layout = [[sg.Text('Please enter the required information below', font = subtitle_font)],
                  [sg.Text("First name:", size = (15, 1)), sg.Input(key = "-FIRST_NAME-")],
                  [sg.Text("Last name:", size = (15, 1)), sg.Input(key = "-LAST_NAME-")],
                  [sg.Text("Adress:", size = (15, 1)), sg.Input(key = "-ADDRESS-")],
                  [sg.Text("Post Number:", size = (15, 1)), sg.Input(key = "-POST_NUMBER-")],
                  [sg.Text('Subscription:', size = (15, 1)),
                   sg.Radio("Paid", "RADIO1", key = '-SUBSCRIPTION-', font = subtitle_font),
                   sg.Radio("Not Paid", "RADIO2", key = '-SUBSCRIPTION-', font = subtitle_font),
                   sg.Push(), sg.Button("CLEAR FIELDS", size = (13, 1))],
                  [sg.Push(),
                   [sg.Text(size = (40, 1), key = '-OUTPUT-')],
                   [sg.Button("CONFIRM", key = "-CONFIRM-", size = (20, 1)),
                    sg.Push(),
                    sg.Button("CANCEL", key = "-CANCEL-", size = (20, 1))],
                   ]]

        window = sg.Window("Add member", layout, modal = True, font = default_font, margins = (60, 60))

        def clear_Input():
            for _ in values:
                window['-FIRST_NAME-'].update('')
                window['-LAST_NAME-'].update('')
                window['-ADDRESS-'].update('')
                window['-POST_NUMBER-'].update('')
            return None



        while True:
            event, values = window.read()
            subscription = 'Paid' if values['-SUBSCRIPTION-'] else 'Not Paid'
            # print(f'The subscription is: {subscription}')

            if event == 'CLEAR FIELDS':
                clear_Input()


            if event == "-CONFIRM-":
                results = validation.validate(values)
                if results["is_valid"]:
                    sg.popup(f"Mr/Mrs : {values['-FIRST_NAME-'].upper()}\nhas Been successfully Added Into Database",
                             font = default_font,
                             background_color = '#098E89', no_titlebar = True)

                else:
                    error_message = validation.generate_error_message(results["values_invalid"])
                    sg.PopupError('You Have Entered', error_message, font = default_font,
                                  background_color = '#098E89', no_titlebar = True, )

                # print('First Name:', values["-FIRST_NAME-"], 'Last Name: ', values["-LAST_NAME-"], 'Address: ',
                #       values["-ADDRESS-"], 'Post Number: ', values["-POST_NUMBER-"],
                #       'Subscription: ', subscription)

                insert_contact(values["-FIRST_NAME-"],
                               values["-LAST_NAME-"],
                               values["-ADDRESS-"],
                               values["-POST_NUMBER-"],
                               subscription
                               )

                break

            elif event == sg.WIN_CLOSED or event == "-CANCEL-":
                break

        window.close()

    @staticmethod
    def view_window():
        conn = sqlite3.connect("OrmDatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members")
        rows = cursor.fetchall()

        def delete(values):
            conn = sqlite3.connect('OrmDatabase.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM members WHERE id_num = ?', (values['-id-'],))
            conn.commit()
            conn.close()

        Search_Frame = [[sg.Button("SEARCH Or REFRESH", key = "-SEARCH-", size = (20, 1)),
                         sg.InputText('', key = '-SEARCH_BOX-', size = (60, 1), tooltip = 'Search')]]
        Delete_Frame = [[sg.Button('DELETE By ID',size = (20, 1)), sg.Input('', s = 5, key = '-id-', size = (60, 1))]]
        Database_Frame = [[sg.Table(
            values = rows,
            headings = ["Member ID", "First Name", "Last Name", "Address", "Post Number", "Subscription"],
            auto_size_columns = False, justification = "center", def_col_width = 12, num_rows = min(len(rows), 10),
            row_height = 35, key = '-TABLE-')]]

        layout = [[sg.Frame('Search, Refresh Or Delete', Search_Frame + Delete_Frame, font = default_font,
                            background_color = background_color, size = (820, 160))],
                  [sg.Push(),sg.Button("CLEAR INPUT FIELDS", size = (20, 1))],
                  [sg.Frame('Your Database ', Database_Frame, font = default_font,
                            background_color = background_color)],
                  [sg.Text(size = (40, 1), font = default_font, key = '-OUTPUT-')],
                  [sg.Button('View Paid Members', size = (20, 1)),
                   sg.Button('View Not Paid Members', size = (20, 1)),
                   sg.Button("EXIT", key = "-EXIT-", size = (20, 1))]]

        window = sg.Window("Members View", layout, modal = True, font = default_font, element_justification = "center",
                           margins = (60, 60))

        def clear_SearchBox():
            for _ in values:
                window['-SEARCH_BOX-'].update('')
                window['-id-'].update('')

            return None
        window.read()

        while True:
            event, values = window.read()
            if event == '-EXIT-' or event == sg.WIN_CLOSED:
                break

            if event == 'CLEAR INPUT FIELDS':
                clear_SearchBox()

            if event == '-SEARCH-':
                search_term = values['-SEARCH_BOX-']
                cursor.execute("SELECT * FROM members WHERE id_num LIKE ?"
                               "OR first_name LIKE ? "
                               "OR last_name LIKE ?",
                               ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
                rows = cursor.fetchall()
                window['-TABLE-'].Update(values = rows)

            if event == 'DELETE':
                print('Deleted successfully')
                window['-OUTPUT-'].update('ID NUMBER ' + values['-id-'] + " : is deleted successfully From Database",
                                          text_color = 'Green', )
                delete(values)
                window['-TABLE-'].Update(values = rows)

            if event == 'View Paid Members':
                # Select all paid subscriptions
                query = 'SELECT * FROM members WHERE subscription = "Paid"'
                cursor.execute(query)
                rows = cursor.fetchall()
                window['-TABLE-'].update(values = rows)

            if event == 'View Not Paid Members':
                # Select all not paid subscriptions
                query = 'SELECT * FROM members WHERE subscription = "Not Paid"'
                cursor.execute(query)
                rows = cursor.fetchall()
                window['-TABLE-'].update(values = rows)

        window.close()
