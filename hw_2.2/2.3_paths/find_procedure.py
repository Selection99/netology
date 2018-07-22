# Задание
# мне нужно отыскать файл среди десятков других
# я знаю некоторые части этого файла (на память или из другого источника)
# я ищу только среди .sql файлов
# 1. программа ожидает строку, которую будет искать (input())
# после того, как строка введена, программа ищет её во всех файлах
# выводит список найденных файлов построчно
# выводит количество найденных файлов
# 2. снова ожидает ввод
# поиск происходит только среди найденных на этапе 1
# 3. снова ожидает ввод
# ...
# Выход из программы программировать не нужно.
# Достаточно принудительно остановить, для этого можете нажать Ctrl + C

# Пример на настоящих данных

# python3 find_procedure.py
# Введите строку: INSERT
# ... большой список файлов ...
# Всего: 301
# Введите строку: APPLICATION_SETUP
# ... большой список файлов ...
# Всего: 26
# Введите строку: A400M
# ... большой список файлов ...
# Всего: 17
# Введите строку: 0.0
# Migrations/000_PSE_Application_setup.sql
# Migrations/100_1-32_PSE_Application_setup.sql
# Всего: 2
# Введите строку: 2.0
# Migrations/000_PSE_Application_setup.sql
# Всего: 1

# не забываем организовывать собственный код в функции
import os.path as p
from os import listdir, chdir

if __name__ == '__main__':
    pass

migrations = 'Migrations'
current_dir = p.dirname(p.abspath(__file__))
chdir(p.join(current_dir, migrations))
# chdir(migrations) # если запустить скрипт из папки, где он лежит

# Вариант 1 абсолютный путь
# results_of_search = [p.abspath(dir) for dir in list(listdir())]
# Вариант 2 относительный путь
results_of_search = listdir()


def print_list_of_files():
    for dir in results_of_search:
        print(dir)
    print("Всего:", len(results_of_search))


def check_condition(file):
    # Через бинарники тоже работает
    # with open(file, 'rb') as f:
    #     if str(f.read().lower()).find(search_arg.lower()) == -1:
    #         return False
    # return True
    with open(file, encoding='utf8', errors='ignore') as f:
        if f.read().lower().find(search_arg.lower()) == -1:
            return False
    return True


# Этот цикл можно переписать в одну строчку, но это уменьшит читаемость
while len(results_of_search) > 1:
    search_arg = input("Введите строку: ")
    results_of_search = [file for file in results_of_search if check_condition(file)]
    print_list_of_files()

# Запросы
# INSERT -> 307 (в примере 301)
# APPLICATION_SETUP -> 26 (здесь уже совпадает)
# A400M -> 17
# 0.0 -> 2
# 2.0 -> 1
