import pip._internal as pip
from Logging import debug, info, warn, error, critical
from Logging import summary_logging


class auto_import():
    libs = {}
    array = []

    def __init__(self, array):
        self.array = array

    def libs_check(self):
        libs = self.libs
        array = self.array
        for lib in array:
            try:
                __import__(lib)  # попытка импортировать библиотеку
                libs[lib] = 1
                info(f'[LIB_CONFIG] --> {lib} is installed')
            except ImportError:
                self.smth_wrong = True
                libs[lib] = 0
                info(f'[LIB_CONFIG] --> {lib} is not installed')


        for keys in libs:
            if libs[keys] == 1:
                print(keys, '-' * (self.nice_alingment(keys)) + 'YES')
            else:
                print(keys, '-' * (self.nice_alingment(keys) + 1) + 'NO')
                self.all_installed = 0

        self.libs = libs

    def nice_alingment(self, word):
        return (30 - len(word))

    def install_libs(self):
        libs = self.libs
        for lib in libs:
            if libs[lib] == 0:
                try:
                    __import__(lib)  # пытаемся импортировать
                    libs[lib] == 1
                    return __import__(lib)
                except ImportError:
                    print(lib, '.....INSTALLING.....')
                    try:
                        pip.main(['install', lib])  # ставим библиотеку если её нет
                        print(f'{lib} succesfully imported')
                        info(f'[LIB_CONFIG] --> {lib} succesfully imported')
                        return __import__(lib)  # возвращаем библиотеку
                    except:
                        print(f'Error occured {lib} is not installed')
                        error(f'[LIB_CONFIG] --> Error occured {lib} is not installed')
                        return 0


def installer(to_import):

    disk = auto_import(to_import)
    disk.libs_check()

    try:
        if disk.smth_wrong:
            info(f'[LIB_CONFIG] --> All libs installed')
            pass
    except AttributeError:

        return True


    while True:
        answer = input('Do u want to install missing? (Y/N) = ')
        if answer == 'Y':
            disk.install_libs()
            disk.libs_check()
            break
        elif answer == 'N':
            print('shutdowning program...')
            exit()
        else:
            print('Answer is not correct, please answer "Y" or "N"')

        return True

def install_reader():
    with open('requirements.txt', 'r') as file:
        libs = [column.split('=')[0] for column in file]
        installer(libs)


def main_installing_func():
    try:
        install_reader()
    except:
        critical(f'[INSTALLING] --> Some modules cannot not be found or installed')
    finally:
        summary_logging(warn, error, critical, 'INSTALLING')

if __name__ == '__main__':
    install_reader()