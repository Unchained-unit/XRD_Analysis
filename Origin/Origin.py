from pathlib import Path
import os

from Logging import debug, info, warn, error, critical
from Logging import summary_logging

import originpro as op


class worksheet():

    def __init__(self, name, type):
        self.name = name
        self.wks = op.new_sheet(type='w', lname=name)
        self.type = type
        debug(f'[ORIGIN] --> worksheet {name}, {type} created')

    def insert_data(self, col, data, name, axis):
        self.wks.from_list(col=col, data=data, lname=name, axis=axis)
        debug(f'[ORIGIN] --> data {name} inserted at {col} column, axis {axis}')

    def last_column(self):
        return self.wks.cols


class graphing():

    def __init__(self, wks, templates_path):
        self.wks = wks.wks
        self.graph_type = wks.type
        self.templates_path = templates_path
        self.name = wks.name
        self.cols = wks.last_column()
        debug(f'[ORIGIN] --> graph {self.name} is deployed')

        match self.graph_type:
            case 'XRD':
                self.graph = op.new_graph(f'{self.name}_gp', self.templates_path['XRD.otp'])
                debug(f'[ORIGIN] --> type {self.graph_type} confirmed')
            case 'params':
                debug(f'[ORIGIN] --> type {self.graph_type} confirmed')
                pass

        self.layers = {}


    def new_layer(self, name):
        self.layers[name] = self.graph[len(self.layers)]
        debug(f'[ORIGIN] --> layer {name} created')
        return self.layers[name]

    def graphing_xrd_curves(self, name):

        layer = self.new_layer(name)

        for i in range(self.cols - 1):
            graph = layer.add_plot(self.wks, colx=0, coly=i + 1)
            graph.colormap = 'Candy'
            graph.set_cmd('-w 1000')


        layer.group()
        layer.rescale()


    def graphing_xrd_params(self):
        pass


    def multigraphing(self, name):

        match self.graph_type:
            case 'XRD':
                self.graphing_xrd_curves(name)
                debug(f'[ORIGIN] --> multigraphing with "XRD" model')
            case 'params':
                debug(f'[ORIGIN] --> multigraphing with "params" model')
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

        try:
            self.TEMPLATES_PATH = {f'{temp}': (f'{Path(__file__).parents[1]}/Templates/{temp}') for temp in
                               os.listdir(f'{Path(__file__).parents[1]}/Templates')}
        except Exception as e:
            error(f'ORIGIN --> Templates cannot be found')
            info(f'[ERROR] --> {e}')

        self.worksheets = {}
        self.graphs = {}
        self.xrds_pack = xrd_session.xrds_pack
        self.normed_curves = xrd_session.all_norm_curves


    def create_ws(self, name, type):
        self.worksheets[name] = worksheet(name, type)
        debug(f'[ORIGIN] --> worksheet {name} created')

    def init_xrd_worksheets(self, type = 'XRD'):
        for angles, values in self.normed_curves.items():
            self.create_ws(f'norm on {angles}', type)
            self.worksheets[f'norm on {angles}'].insert_data(0, self.xrds_pack[0].x_values, '2Thetta', axis='X')
            for i, name, xrd_pattern in zip(range(len(values)), values.keys(), values.values()):
                self.worksheets[f'norm on {angles}'].insert_data(i+1, xrd_pattern.y_values, name, axis='Y')
                debug(f'[ORIGIN] --> {len(xrd_pattern.y_values), xrd_pattern.y_values}')


    def xrd_insertion(self, name):
        self.worksheets[name].insert_data(0, self.xrds_pack[0].x_values, '2Thetta', axis='X')
        for i in range(len(self.xrds_pack)):
            self.worksheets[name].insert_data(i+1, self.xrds_pack[i].y_values, self.xrds_pack[i].name, axis='Y')

            debug(f'[ORIGIN] --> data for {self.xrds_pack[i].name} inserted')


    def wks_graphing(self, wks, name):
        self.graphs[f'{name}_gr'] = graphing(wks, self.TEMPLATES_PATH)
        debug(f'[ORIGIN] --> {name}_gr is graphing now')
        self.graphs[f'{name}_gr'].multigraphing(f'{name}_gr')
        debug(f'[ORIGIN] --> multy ready')


    def full_graphing(self):
        for name, wks in self.worksheets.items():
            self.wks_graphing(wks, name)



    def show(self):
        if op.oext:
            op.set_show(True)


def origin_func(xrd_session):
    try:
        origin_running_session = origin_session(xrd_session)
        info('[ORIGIN] --> Session is running successfully ')
        origin_running_session.create_ws('Non - Normalized', type='XRD')
        origin_running_session.xrd_insertion('Non - Normalized')
        origin_running_session.init_xrd_worksheets()

        origin_running_session.full_graphing()

        origin_running_session.show()

        return origin_running_session
    except:
        critical('[ORIGIN] --> Session can not be initialized')
        op.exit()



def origin_main_func(xrd_session):
    try:
        ORS = origin_func(xrd_session)
        debug(f'[ORIGIN] --> Origin is working properly')
        return ORS
    except Exception as e:
        op.exit()
        critical(f'[ORIGIN] --> Origin module stopped working')
        error(f'[ORIGIN] --> {e}')

    finally:
        summary_logging(warn, error, critical, 'ORIGIN')

if __name__ == '__main__':
    origin_main_func()
