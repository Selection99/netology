from glob import glob
import json

words_dictionary = {}
list_of_files = glob('Source/*.json')


def try_add_to_result_dict(text):
    for str in text.split():
        if len(str) > 6:
            try:
                words_dictionary[str] += 1
            except:
                words_dictionary[str] = 1


def iterating_json(big_obj):
    for obj in big_obj.values():
        if isinstance(obj, str):
            try_add_to_result_dict(obj)
        elif isinstance(obj, dict):
            iterating_json(obj)
        elif isinstance(obj, list):
            for small_obj in obj:
                iterating_json(small_obj)
        else:
            print(f"{type(obj)}: {obj}")
            raise Exception("Strange. Check obj.", obj)


for file in list_of_files:
    with open(file, encoding='utf8', errors='ignore') as f:
        iterating_json(json.load(f))
for i, word in enumerate(sorted(list(words_dictionary.items()), key=lambda tupl:tupl[1], reverse=True)[:10]):
    print(f'{i + 1}) "{word[0]}" - {word[1]}')
