from Logging import debug, info, warn, error, critical
import originpro as op

class worksheet():

    def __init__(self, name):
        self.name = name
        self.wks = op.new_sheet(type='w', lname=name)

    def insert_data(self, col, data, name, axis):
        self.wks.from_list(col=col, data=data, lname=name, axis=axis)


class graph():

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
            debug(f"Текущая версия Origin: {version}")

            # Проверяем, поддерживается ли версия
            if version < min_supported_version:
                error(
                    f"Предупреждение: Текущая версия Origin ({version}) ниже минимально поддерживаемой ({min_supported_version}).")
            else:
                debug("Версия Origin поддерживается.")

        except Exception as e:
            error(f"Произошла ошибка при проверке версии Origin: {e}")

    def __init__(self):
        self.check_origin_version()

        pass
        # wks_original = op.new_sheet(type='w', lname='XRD_orig')
        # wks_peak_normalize = op.new_sheet(type='w', lname='XRD_orig')
        # wks_normalize_FTO = op.new_sheet(type='w', lname='XRD_orig')


    def show(self):
        if op.oext:
            op.set_show(True)


if __name__ == '__main__':
    a = origin_session()
    w_k_s = worksheet(name='commited')
    print(w_k_s.name)
    a.show()
