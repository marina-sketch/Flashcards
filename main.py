import PySimpleGUI as sg
import xlrd
import pandas as pd
import time

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

    # -------  Begin Flashcard Window  --------
    if ev1 == 'Start'  and not win2_active:
        win2_active = True
        win1.Hide()

        loc = val['Browse']

        # Read File
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        dataframe = pd.read_excel(loc, sheet_name = 0)
        x = 0

        # Prepare Deck
        count_row = dataframe.shape[0]
        count_col = dataframe.shape[1]
        if count_col > 4:
            dataframe.drop(dataframe.columns[[0]], axis=1, inplace=True)
        deck = dataframe.sort_values(by='Weight',ascending=False)

        # Printing Out Window (Layout)
        layout2 = [[sg.Text(' ', size=(80, 10), font = ('Helvetica', 12), justification='center', key='_SPACE_')],
        [sg.Text(deck.iat[x, 0], size=(40, 2), justification='center', font = ('Helvetica', 20), key='_VOCAB_'),
        sg.Text(' ', font = ('Helvetica', 16), size=(40, 2), justification='center', key='_DEF_')],
        [sg.Text(' ', size=(80, 10), font = ('Helvetica', 12), justification='center', key='_HINT_')],
        [sg.Button('Done')]]

        win2 = sg.Window('Study Time', layout2, resizable=True, finalize=True, return_keyboard_events = True)
        win2['_VOCAB_'].expand(True, True, True)
        win2['_DEF_'].expand(True, True, True)
        win2['_HINT_'].expand(True, True, True)

        # ------------- Flashcard Mode-----------------
        definition = ' '
        hint = ' '
        clear = False
        tic = time.perf_counter()
        while True:
            ev2, val2 = win2.Read()
            toc = time.perf_counter()
            print(ev2) # testing out outputs

            # Prev Word
            if ev2 == 'Left:37' and (x - 1) >= 0:
                deck.at[x, 'Weight'] = deck.at[x, 'Weight'] + toc - tic
                tic = toc
                x = x - 1
                clear = True

            # Hide Definition
            if ev2 == 'Up:38':
                definition = deck.iat[x, 1]

            # Next Word
            if ev2 == 'Right:39':
                deck.at[x, 'Weight'] = deck.at[x, 'Weight'] + toc - tic
                tic = toc
                x = x + 1
                clear = True

            # Show Hint
            if ev2 == 'Down:40':
                hint = deck.iat[x, 3]

            # Exit Flashcard Mode
            if ev2 == sg.WIN_CLOSED or ev2 == 'Done' or x >= count_row:

                # Write to File
                with pd.ExcelWriter(loc) as fileName:
                    deck.to_excel(fileName)

                # Exit to Prev Window
                win2.Close()
                win2_active = False
                win1.UnHide()
                break

            # Update Flashcard
            if clear is True:
                definition = ' '
                hint = ' '
                clear = False
            word = deck.iat[x, 0]

            win2.Element('_VOCAB_').Update(word)
            win2.Element('_DEF_').Update(definition)
            win2.Element('_HINT_').Update(hint)
