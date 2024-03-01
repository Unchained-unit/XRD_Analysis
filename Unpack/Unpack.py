from Logging import debug, info, warn, error, critical
import os
class package():
    def __init__(self):

        # Получаем список всех файлов и директорий в текущей директории
        all_entries = os.listdir('.')

        # Фильтруем список, оставляя только файлы, исключая 'README.txt' и 'main.py'
        file_names = [entry for entry in all_entries if
                      os.path.isfile(entry) and entry not in ['README.txt', 'main.py', 'py_log.log']]

        # Возвращаем массив названий файлов
        self.file_names = file_names
        debug("package --- constructed")

    def to_much(self):
        pass

if __name__ == '__main__':
    a = package()
    print(a.file_names)
