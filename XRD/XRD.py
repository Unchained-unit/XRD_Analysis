import numpy as np
from scipy.signal import find_peaks_cwt
from scipy.optimize import curve_fit

from Logging.Logging import debug, info, warn, error, critical
from Unpack.Unpack import package

class Tpeak():

    def __init__(self, peak_index, x_values, y_values, name):
        self.name = name
        self.pos = x_values[peak_index]
        self.x_list = [x_values[x] for x in range(peak_index-20, peak_index+21)]
        self.y_list = [y_values[x] for x in range(peak_index-20, peak_index+21)]
        debug(f'[XRD] --> x_values for peak at {x_values[peak_index]} - {self.x_list}')
        debug(f'[XRD] --> y_values for peak at {x_values[peak_index]} - {self.y_list}')

    def lorentzian(self, x, A, x0, gamma):
        return A / (1 + ((x - x0) / gamma) ** 2)

    def fit_lorentzian(self):
        x_values = self.x_list
        y_values = self.y_list
        # Начальные параметры: A, x0, gamma
        initial_params = [max(y_values), x_values[np.argmax(y_values)], np.std(x_values)]

        # Попытка фитирования
        try:
            params, covariance = curve_fit(self.lorentzian, x_values, y_values, p0=initial_params)
            # Вычисление стандартных ошибок параметров из ковариационной матрицы
            errors = np.sqrt(np.diag(covariance))

            self.params = params
            self.errors = errors
            debug(f'[XRD] --> {self.name} peak at {self.pos} params {params} errors {errors}')

        except RuntimeError:
            error(f'[XRD] --> Params cannot be optimized - Zeros are returned')
            self.params = [0,0,0]
            self.errors = [0,0,0]


class XRD_pattern():

    def __init__(self, xrd_dict, name):

        self.x_values = []
        self.y_values = []
        self.name = name

        self.pattern_peaks = []

        for keys, values in xrd_dict.items():

            self.x_values.append(keys)
            self.y_values.append(values)
        debug(f'[XRD] --> x and y values are formed for {self.name}')
        #print(self.x_values)

        self.AVERAGE = sum(self.y_values)/len(self.y_values)
        self.DISPERSION = sum([(y - self.AVERAGE)**2 for y in self.y_values])/len(self.y_values)
        debug('[XRD] --> basics are found')

    def find_peaks_with_wavelet(self, widths=np.arange(1, 50)):
        # Преобразуем списки в массивы NumPy
        x = np.array(self.x_values)
        y = np.array(self.y_values)


        threshold = self.AVERAGE + 0.5*np.sqrt(self.DISPERSION)
        # print('threshold is set', threshold)

        # Ищем пики с использованием вейвлет-преобразования
        peaks = find_peaks_cwt(y, widths)

        # Отфильтруем пики по порогу
        peaks = [peak for peak in peaks if y[peak] > threshold]

        self.Peaks_index, self.Peaks = peaks, y[peaks]
        debug(f'[XRD] --> peaks of {self.name} were found {self.Peaks}')

    def peaks(self, peaks_list):
        for peak in peaks_list:
            self.pattern_peaks.append(Tpeak(peak, self.x_values, self.y_values, self.name))
        for peak in self.pattern_peaks:
            peak.fit_lorentzian()

class XRD_pack():

    def __init__(self, xrds, names):
        self.names = names
        self.xrds_pack = [XRD_pattern(xrd, name) for xrd, name in zip(xrds, names)]

        info(f'[XRD] --> XRD_pack is formed from {names}')


    def cross_peak(self):
        for xrd in self.xrds_pack:
            xrd.find_peaks_with_wavelet()

        peaks_index = [x.Peaks_index for x in self.xrds_pack]
        self.max_peak_index = (sorted(peaks_index, key = lambda x: len(x)))[-1]
        info(f'[XRD] --> {self.max_peak_index} peaks is going to be examined')

    def find_params(self):
        for xrd in self.xrds_pack:
            xrd.peaks(self.max_peak_index)


    def imprint(self):
        for xrd in self.xrds_pack:
            print(xrd.Peaks_index)
            print(xrd.Peaks)


if __name__ == '__main__':
    from Unpack.Unpack import package
    a = XRD_pack()
