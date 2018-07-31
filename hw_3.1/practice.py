import requests
from glob import glob
from os.path import basename, join


def translate_text(text, initial_lang, result_lang):
    """
    YANDEX translation plugin

    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/

    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :param text: <str> text for translation.
    :return: <str> translated text.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20180731T203541Z.6b6d2b746fb5168c.de806e4445b832f9e1afa70abfb4ffa5ff51794f'

    params = {
        'key': key,
        'lang': f"{initial_lang}-{result_lang}",
        'text': text,
    }
    response = requests.get(url, params=params).json()
    return ' '.join(response.get('text', []))


def translate_file(initial_dir, result_dir, initial_lang, result_lang = 'ru'):
    print(initial_dir, result_dir, initial_lang, result_lang)
    with open(initial_dir) as f:
        result = translate_text(f.read(), initial_lang, result_lang)
    with open(result_dir, 'w') as f:
        f.write(result)


def execute_task():
    for file in glob('Source/*'):
        filename = basename(file)
        translate_file(file, join('Result', filename), filename.partition('.')[0].lower())


execute_task()
