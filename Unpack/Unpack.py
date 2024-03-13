from Logging import debug, info, warn, error, critical
import os
class package():
    def __init__(self):

        # Получаем список всех файлов и директорий в текущей директории
        all_entries = os.listdir('.')

        # Фильтруем список, оставляя только файлы, исключая 'README.txt' и 'main.py'
        file_names = [entry for entry in all_entries if
                      os.path.isfile(entry) and entry not in ['README.txt', 'main.py', 'py_log.log', 'requirements.txt']]

        # Возвращаем массив названий файлов
        self.file_names = file_names
        debug("[Unpacking] --> package constructed")

    def to_much(self):
        if len(self.file_names) >= 10:
            warn('[Unpacking] --> This might be a lot of files to operate')
            return False
        debug('[Unpacking] --> package is small enough to operate')
        return True

    def sort_by(self):
        if len(self.file_names) == 0:
            error('[Unpacking] --> List of XRD`s is empty this might cause me a little trouble')
        debug('[Unpacking] --> List is not empty')
        try:
            self.s_file_names = sorted(self.file_names, key=lambda x: int(x[4:].split('-')[0]))
        except:
            self.s_file_names = sorted(self.file_names, key=lambda x: int(x[:-1].split('#')[0]))
        finally:
            warn('[Unpacking] --> list cannot be sorted it will stay unchanged')
            self.s_file_names = self.file_names
            return False

    def unpack(self):
        self.unpacked_files = []
        for txtfile in self.s_file_names:
            tmp_dict = dict()
            err = 0
            with open(txtfile, 'r') as file:
                for column in file:
                    if column == '\n':
                        pass
                    else:
                        try:
                            tmp_dict[float(column.split()[0])] = float(column.split()[1])
                        except:
                            err += 1
            self.unpacked_files.append(tmp_dict)
            if err == 0:
                debug(f"[Unpacking] --> {txtfile} was unpacked")
            else:
                error(f'[Unpacking] --> {txtfile} is corrupted {err} lines skipped')
        info("[Unpacking] --> Package was fully unpacked")
        return True

    def files_check(self):
        first_values = [next(iter(diction.keys())) for diction in self.unpacked_files]
        delta_values = [list(diction)[1] - list(diction)[0] for diction in self.unpacked_files]
        len_values = [len(diction) for diction in self.unpacked_files]

        if len(set(first_values)) != 1:
            warn('[Unpacking] --> first values of input files are different')
            return False

        if len(set(delta_values)) != 1:
            warn('[Unpacking] --> delta value of input files are different')
            return False

        if len(set(len_values)) != 1:
            warn('[Unpacking] --> length of input files are different')
            return False

        debug('[Unpacking] --> All files have same first values, delta value, length')
        return True


if __name__ == '__main__':
    a = package()
    print(a.file_names)
