import PySimpleGUI as sg
import xlrd
import pandas as pd

layout = [[sg.Text('Choose A File', size=(35, 1))],
        [sg.InputText('Default Folder'), sg.FileBrowse()], [sg.Button('Start'), sg.Button('Exit')]]

win1 = sg.Window('Main Menu', layout)
win2_active = False



while True:
    ev1, val = win1.Read(timeout=100)

    # End Application
    if ev1 == sg.WIN_CLOSED or ev1 == 'Exit':
        print(ev1)
        win1.Close()
        break

    # -------  Begin Second Window  --------
    if ev1 == 'Start'  and not win2_active:
        win2_active = True
        win1.Hide()

        loc = val['Browse']

        # Read File
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        dataframe = pd.read_excel(loc, sheet_name = 0)
        print(dataframe)
        x = 0

        # Run Algorithm
        dataframe.sort_values(by=['Weight'])
        deck = dataframe

        # Printing Out Window (Layout)
        layout2 = [[sg.Text(deck.iat[x, 0], size=(40, None), justification='center', font = ('Helvetica', 20), key='_VOCAB_'),
            sg.Text(' ', size=(40, 40), justification='center', key='_DEF_')], [sg.Button('Done')]]

        win2 = sg.Window('Study Time', layout2, resizable=True, finalize=True, return_keyboard_events = True)
        win2['_VOCAB_'].expand(True, True, True)
        win2['_DEF_'].expand(True, True, True)


        # ------------- Flashcard Mode-----------------
        definition = ' '
        while True:
            ev2, val2 = win2.Read()

            print(ev2) # testing out outputs

            # Prev Word
            if ev2 == 'Left:37' and (x - 1) >= 0:
                x = x - 1
                definition = ' '

            # Hide Definition
            if ev2 == 'Up:38':
                definition = ' '

            # Next Word
            if ev2 == 'Right:39':
                x = x + 1
                definition = ' '

            # Show Definition
            if ev2 == 'Down:40':
                definition = deck.iat[x, 1]

            # Update Flashcard
            word = deck.iat[x, 0]
            win2.Element('_VOCAB_').Update(word)
            win2.Element('_DEF_').Update(definition)

            # Exit Flashcard Mode
            if ev2 == sg.WIN_CLOSED or ev2 == 'Done':

                # Algorithm

                # Write to File

                # Exit to Prev Window
                win2.Close()
                win2_active = False
                win1.UnHide()
                break
