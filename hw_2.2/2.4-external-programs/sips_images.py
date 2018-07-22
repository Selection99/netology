from os import path as p
from subprocess import Popen, PIPE

# FOR MAC OS

dir_name = p.dirname(__file__)
result_dir = p.join(dir_name, 'Result')

command_sips = "sips --resampleWidth 200"
if not p.exists(result_dir):
    with Popen(f"mkdir {result_dir}", shell=True, stderr=PIPE, stdout=PIPE) as proc:
        if proc.stderr.read():
            raise Exception("Failed to create directory")
while True:
    file = input('Введите имя(image.jpg) из папки Source, живущей по соседству с файлом: ')
    file_in_source = p.join(dir_name, 'Source', file)
    file_in_result = p.join(result_dir, file)
    error = ""
    try:
        with Popen(f"cp {file_in_source} {file_in_result}", shell=True, stderr=PIPE, stdout=PIPE) as proc:
            buff = proc.stderr.read()
            if buff:
                error += buff.decode('UTF-8')
                raise Exception("Failed to copy file")
        with Popen(f"sips --resampleWidth 200 {file_in_result}", shell=True, stderr=PIPE, stdout=PIPE) as proc:
            buff = proc.stderr.read()
            raise Exception()
            if proc.returncode:
                error += buff.decode('UTF-8')
                raise Exception("Failed to change file")
        print("Успешно")
    except:
        print("Ошибка:", error.strip())

