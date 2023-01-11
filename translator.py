import requests
import re
import os
import json


def connection():
    try:
        return True if requests.get('https://www.google.com') else False
    except requests.exceptions.ConnectionError:
        return False


def status():
    # check connection to apis and google
    urls = {"Linguee": 'https://linguee-api.fly.dev/api/v2/translations?query=hello&src=en&dst=fr&guess_direction=false&follow_corrections=always',
            'Google': 'https://translate.google.com/m?sl=en&tl=en}&hl=en&q=word',
            'Dictionary': 'https://api.dictionaryapi.dev/api/v2/entries/en/word'}
    for k, v in urls.items():
        try:
            r = requests.get(v)
            print(k, 'Online' if r.status_code == 200 else f'Error {r.status_code}')
        except requests.exceptions.ConnectionError:
            print(k, 'Offline')


def translate(word: str):
    ling_translation, gl_translation, examples = [], [], []
    phonetics, meanings, synonyms, antonyms = {}, {}, [], []
    params = {'query': word,
              'src': from_lang,
              'dst': to_lang,
              'guess_direction': direction,
              'follow_corrections': corrections}

    # get results from linguee
    ling_req_meanings = requests.get('https://linguee-api.fly.dev/api/v2/translations', params=params).json()
    if ling_req_meanings and all([x not in ling_req_meanings for x in ['message', 'detail']]):
        # get max_trs or fewer meanings from British and American dicts
        for content in ling_req_meanings:
            ling_translation += [el['text'] for index, el in enumerate(content['translations']) if index < max_trs]
        # and max_exs or fewer examples
        ling_req_examples = requests.get('https://linguee-api.fly.dev/api/v2/examples', params=params).json()
        examples += [f"{content['text']} ({content['translations'][0]['text']})"
                     for index, content in enumerate(ling_req_examples) if index < max_exs]

    # get results from simple google translator
    gl_req = requests.get(f'https://translate.google.com/m?sl={from_lang}&tl={to_lang}&hl={to_lang}&q={word}').text
    gl_translation = re.findall(r'"result-container">(.*?)</div>', gl_req)

    # get phonetics, meanings, synonyms, antonyms
    html = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}").json()
    try:
        for i in html[0]["phonetics"]:
            if 'text' in i:
                phonetics = [i['text']]
                break
        for dicts in html:
            for i in dicts["meanings"]:
                if i['partOfSpeech'] not in meanings:
                    meanings[i['partOfSpeech']] = [k['definition'] for k in i['definitions']]
                else:
                    meanings[i['partOfSpeech']] += [k['definition'] for k in i['definitions']]
                synonyms += i['synonyms']
                antonyms += i['antonyms']
    except KeyError:
        pass

    return {
        'translation': [gl_translation[0].lower()] + [x.lower() for x in ling_translation if x not in gl_translation],
        'examples': examples,
        'phonetics': phonetics if get_phonetics else '',
        'meanings': meanings if get_meanings else [],
        'synonyms': synonyms[:max_lexis] if get_lexis else [],
        'antonyms': antonyms[:max_lexis] if get_lexis else []
    }


def add_word(translation: dict):
    words = get_words()
    if list(translation)[0] not in words:
        with open('dictionary.json', 'w') as j:
            json.dump(words | translation, j)
        return True
    return False


def delete_word(key):
    words = get_words()
    del words[key]
    with open('dictionary.json', 'w') as j:
        json.dump(words, j)


def get_words():
    with open('dictionary.json') as j:
        try:
            return json.load(j)
        except json.decoder.JSONDecodeError:
            return {}


def save_settings(settings: dict):
    with open('settings.json', 'w') as j:
        json.dump(settings, j)
    load_settings()


def load_settings():
    global options, to_lang, from_lang, corrections, direction, get_phonetics, get_meanings, get_lexis, max_trs, max_exs, max_lexis, max_display
    for i in os.scandir('.'):
        if i.name == 'settings.json':
            with open('settings.json') as j:
                options = json.load(j)
                to_lang, from_lang, corrections, direction, get_phonetics, get_meanings, get_lexis, max_trs, max_exs, max_lexis, max_display = options.values()


if __name__ == 'translator':
    load_settings()
