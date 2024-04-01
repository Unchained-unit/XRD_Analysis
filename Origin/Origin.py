from Logging import debug, info, warn, error, critical
from Logging import summary_logging
import originpro as op

class worksheet():

    def __init__(self, name):
        self.name = name
        self.wks = op.new_sheet(type='w', lname=name)

    def insert_data(self, col, data, name, axis):
        self.wks.from_list(col=col, data=data, lname=name, axis=axis)



class graph():

    def __init__(self):
        pass

class origin_session():

    def check_origin_version(self):
        """
        Проверяет версию установленного Origin и выдает предупреждение,
        если версия ниже минимально поддерживаемой.
        """
        min_supported_version = 9.8

        try:
            # Получаем версию Origin
            version = float(op.lt_float('@V'))
            debug(f"[Origin] -> Текущая версия Origin: {version}")

            # Проверяем, поддерживается ли версия
            if version < min_supported_version:
                error(
                    f"[Origin] -> Предупреждение: Текущая версия Origin ({version}) ниже минимально поддерживаемой ({min_supported_version}).")
            else:
                debug("[Origin] -> Версия Origin поддерживается.")

        except Exception as e:
            error(f"[Origin] -> Произошла ошибка при проверке версии Origin: {e}")

    def __init__(self, xrd_session):
        self.check_origin_version()
        self.graphs = {}
        self.worksheets = {}
        self.xrds_pack = xrd_session.xrds_pack
        pass

    def create_ws(self, name):
        self.worksheets[name] = worksheet(name)

    def init_worksheets(self):
        for keys, values in self.xrds_pack[0].pattern_peaks.items():
            self.create_ws(f'norm on {self.xrds_pack[0].x_values[int(keys)]}')

    def xrd_insertion(self, name):
        self.worksheets[name].insert_data(0, self.xrds_pack[0].x_values, '2Thetta', axis='X')
        for i in range(len(self.xrds_pack)):
            self.worksheets[name].insert_data(i+1, self.xrds_pack[i].y_values, self.xrds_pack[i].name, axis='Y')


    def show(self):
        if op.oext:
            op.set_show(True)



def origin_main_func(xrd_session):
    origin_running_session = origin_session(xrd_session)

    origin_running_session.create_ws('Non - Normalized')
    origin_running_session.xrd_insertion('Non - Normalized')

    origin_running_session.init_worksheets()

    origin_running_session.show()

    summary_logging(warn, error, critical, 'ORIGIN')
    return origin_running_session

if __name__ == '__main__':
    origin_main_func()
