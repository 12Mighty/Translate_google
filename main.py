import PySimpleGUI as sg
import requests
import tkinter as tk

sg.theme('DarkAmber')

language_names = {
    'en': 'Английский', 'de': 'Немецкий', 'fr': 'Французский', 'es': 'Испанский',
    'it': 'Итальянский', 'pt': 'Португальский', 'pl': 'Польский', 'ja': 'Японский',
    'da': 'Датский', 'cs': 'Чешский', 'zh': 'Китайский'
}

layout = [
    [sg.Text('Введите текст на русском языке:')],
    [sg.InputText(key='-INPUT-')],
    [sg.Button('Перевести')],
    [sg.Text('Переводы:', size=(20, 1))],
    [sg.Listbox([], size=(40, 10), key='-OUTPUT-')],
    [sg.Button('Копировать'), sg.Button('Выход')]
]

window = sg.Window('Переводчик', layout)

def translate_text(text, target_lang):
    url = 'https://translate.googleapis.com/translate_a/single'
    params = {'client': 'gtx', 'sl': 'ru', 'tl': target_lang, 'dt': 't', 'q': text}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()[0][0][0]
        return 'Ошибка при переводе'
    except Exception as e:
        return str(e)

translations = []

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Выход'):
        break
    if event == 'Перевести':
        text = values['-INPUT-']
        target_languages = list(language_names.keys())
        translations = [f"{language_names[lang]}: {translate_text(text, lang)}" for lang in target_languages]
        window['-OUTPUT-'].update(values=translations)
    if event == 'Копировать':
        selected_index = window['-OUTPUT-'].get_indexes()
        if selected_index:
            selected_translation = translations[selected_index[0]]
            root = tk.Tk()
            root.withdraw()
            root.clipboard_clear()
            root.clipboard_append(selected_translation)
            root.update()
            root.destroy()

window.close()
