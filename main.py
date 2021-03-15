import PySimpleGUI as sg
import xlsxwriter
import pandas as pd
import time

layout = [[sg.Button('New Deck'), sg.Button('Edit Deck')], [sg.Text('Choose A File', size=(35, 1))],
        [sg.InputText('Default Folder'), sg.FileBrowse()], [sg.Button('Start'), sg.Button('Exit')]]

win1 = sg.Window('Main Menu', layout)
win2_active = False
win3_active = False

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

        # Read File
        loc = val['Browse']
        dataframe = pd.read_excel(loc, sheet_name = 0)
        x = 0

        # Prepare Deck
        count_row = dataframe.shape[0]
        count_col = dataframe.shape[1]
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
        tic = time.perf_counter()
        while True:
            ev2, val2 = win2.Read()
            toc = time.perf_counter()
            print(ev2) # testing out outputs

            # Show Hint
            if ev2 == 'Left:37':
                hint = deck.iat[x, 3]

            # Hide Definition
            if ev2 == 'Up:38':
                definition = ' '

            # Show Definition
            if ev2 == 'Down:40':
                definition = deck.iat[x, 1]

            # Next Word
            if ev2 == 'Right:39':
                deck.at[x, 'Weight'] = deck.at[x, 'Weight'] + toc - tic
                tic = toc
                x = x + 1
                definition = ' '
                hint = ' '

            # Exit Flashcard Mode
            if ev2 == sg.WIN_CLOSED or ev2 == 'Done' or x >= count_row:

                # Write to File
                with pd.ExcelWriter(loc) as fileName:
                    deck.to_excel(fileName, index=False)

                # Exit to Prev Window
                win2.Close()
                win2_active = False
                win1.UnHide()
                break

            # Update Flashcard
            word = deck.iat[x, 0]
            win2.Element('_VOCAB_').Update(word)
            win2.Element('_DEF_').Update(definition)
            win2.Element('_HINT_').Update(hint)


    # -------  Create Flashcard Window  --------
    if ev1 == 'New Deck'  and not win3_active:
        win3_active = True
        win1.Hide()

        # Printing Out Window (Layout)
        layout3 = [[sg.Text(' ', size=(80, 10), font = ('Helvetica', 12), justification='center', key='_SPACE_')],
        [sg.Text(' ', size=(40, 2), justification='center', font = ('Helvetica', 20), key='_VOCAB_'),
        sg.Text(' ', font = ('Helvetica', 16), size=(40, 2), justification='center', key='_DEF_')],
        [sg.Text(' ', size=(80, 10), font = ('Helvetica', 12), justification='center', key='_HINT_')],
        [sg.Text('Vocab: ', key='_VIn_'), sg.InputText(size=(70,1)), sg.Text('Def: ', key='_DIn_'), sg.InputText(size=(70,1))],
        [sg.Button('Done')]]

        layout4 = [[sg.Text(' ', size=(80, 10), font = ('Helvetica', 12), justification='center', key='_SPACE_')],
        [sg.Text(' ', size=(40, 2), justification='center', font = ('Helvetica', 20), key='_VOCAB_'),
        sg.Text(' ', font = ('Helvetica', 16), size=(40, 2), justification='center', key='_DEF_')],
        [sg.Text(' ', size=(80, 10), font = ('Helvetica', 12), justification='center', key='_HINT_')],
        [sg.Text('Vocab: ', key='_VIn_'), sg.InputText(size=(70,1)), sg.Text('Def: ', key='_DIn_'), sg.InputText(size=(70,1))],
        [sg.Button('Done')]]

        win3 = sg.Window('New Deck', layout3, resizable=True, finalize=True, return_keyboard_events = True)

        column_names = ["Vocab", "Def", "Weight", "Hint"]
        df = pd.DataFrame(columns=column_names)
        x = False

        while True:
            ev3, val3 = win3.Read()

            # Exit Flashcard Mode
            if ev3 == sg.WIN_CLOSED or ev3 == 'Exit':

                # Write to New File
                if x is True:
                    workbook = xlsxwriter.Workbook('')
                    worksheet = workbook.add_worksheet()

                    worksheet.write(0, 0, 'Vocab')
                    worksheet.write(0, 1, 'Def')
                    worksheet.write(0, 2, 'Weight')
                    worksheet.write(0, 3, 'Hint')

                    row = 1
                    for v, d, w, h in df:
                        worksheet.write(row, 0, v)
                        worksheet.write(row, 1, d)
                        worksheet.write(row, 2, w)
                        worksheet.write(row, 3, h)
                        row += 1

                    workbook.close()

                # Exit to Prev Window
                win3.Close()
                win3_active = False
                win1.UnHide()
                break
