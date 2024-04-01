import numpy as np
from scipy.signal import find_peaks_cwt
from scipy.optimize import curve_fit

from Logging import debug, info, warn, error, critical
from Logging import summary_logging
from Unpack.Unpack import package

'''EN
In that module 3 classes
XRD_pack - represents all data in 1 place, that will be used in inserting data in origin
XRD_patter - the class representing single graph with all it peaks
TPeak - lowest structure almost a dataclass, used to fit 1 peak

So XRD_pack is operating with large amounts of XRD_pattern samples and
XRD_pattern is operating with large amounts of TPeak samples
'''
class Tpeak():
    def __init__(self, peak_index, x_values, y_values, name):
        self.name = name
        self.pos = x_values[peak_index]
        #Peak fitted with values of x and y in radius 20 from peak point founded
        #It can be variable values 20 is just my guess
        self.x_list = [x_values[x] for x in range(peak_index-20, peak_index+21)]
        self.y_list = [y_values[x] for x in range(peak_index-20, peak_index+21)]
        debug(f'[XRD] --> x_values for peak at {x_values[peak_index]} - {self.x_list}')
        debug(f'[XRD] --> y_values for peak at {x_values[peak_index]} - {self.y_list}')

    def lorentzian(self, x, A, x0, gamma):
        #Pseudo-Voight is not used in case that all my tries with it
        #end up fititin very-badly with significantly larger error
        #U can try rewrite it for Pseudo-Voight
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

        self.pattern_peaks = dict()

        for keys, values in xrd_dict.items():

            self.x_values.append(keys)
            self.y_values.append(values)
        debug(f'[XRD] --> x and y values are formed for {self.name}')
        #DISPERTION and AVG is needed to evaluate threshold to separate peaks
        self.AVERAGE = sum(self.y_values)/len(self.y_values)
        self.DISPERSION = sum([(y - self.AVERAGE)**2 for y in self.y_values])/len(self.y_values)

        debug(f'[XRD] --> Dispersion {self.DISPERSION} was found')

    def find_peaks_with_wavelet(self, widths=np.arange(1, 50)):
        #I think this is one of the hardest parts, i found wavelet to be
        #the best for XRD, maybe there is smth better

        x = np.array(self.x_values)
        y = np.array(self.y_values)

        KOEFFICIENT = 0.5
        #This is arguable koefficient i think in web interface it will
        #be variable but here 0.5 is working great

        threshold = self.AVERAGE + KOEFFICIENT*np.sqrt(self.DISPERSION)

        #Just find peaks with scipy lib
        peaks = find_peaks_cwt(y, widths)

        #Filtering with threshold
        peaks = [peak for peak in peaks if y[peak] > threshold]

        self.Peaks_index, self.Peaks = peaks, y[peaks]
        debug(f'[XRD] --> peaks of {self.name} were found {self.Peaks_index}')

    def peaks(self, peaks_list):
        #Init Tpeak classes
        for peak in peaks_list:
            self.pattern_peaks[f'{peak}'] = (Tpeak(peak, self.x_values, self.y_values, self.name))
        #Fitting every peak
        for keys, values in self.pattern_peaks.items():
            values.fit_lorentzian()

    def norm_on_peak(self):
        self.norm_xrds = dict()
        for keys, values in self.pattern_peaks.items():
            try:
                self.norm_xrds[f'{keys}'] = [y/values.params[0] for y in self.y_values]
                debug(f'[XRD] --> {self.name} is normalized on peak at {self.x_values[int(keys)]}')
            except ZeroDivisionError:
                info(f'{self.name} is NOT normalized on peak at {self.x_values[int(keys)]}, peak is not identified')


class XRD_pack():

    def __init__(self, xrds, names):
        #Names are usefull to debug and also will be injected in origin column names
        self.names = names
        self.xrds_pack = [XRD_pattern(xrd, name) for xrd, name in zip(xrds, names)]

        info(f'[XRD] --> XRD_pack is formed from {names}')


    def cross_peak(self):
        #Finding peaks
        for xrd in self.xrds_pack:
            xrd.find_peaks_with_wavelet()

        #This is also quite problematic feature it is obvious that even if u
        #put nearly same graph founed peaks will be different
        #so my solution just to take the biggest array and find that peaks in every graph
        peaks_index = [x.Peaks_index for x in self.xrds_pack]
        self.max_peak_index = (sorted(peaks_index, key = lambda x: len(x)))[-1]
        info(f'[XRD] --> {self.max_peak_index} peaks is going to be examined')

    def find_params(self):
        #Initializating finding params
        for xrd in self.xrds_pack:
            xrd.peaks(self.max_peak_index)

    def norm_all_curves(self):
        for xrd in self.xrds_pack:
            xrd.norm_on_peak()


    def imprint(self):
        for xrd in self.xrds_pack:
            print(xrd.Peaks_index)
            print(xrd.Peaks)


def xrd_main_func(files, names):
    xrd_session = XRD_pack(files, names)
    xrd_session.cross_peak()
    xrd_session.find_params()
    xrd_session.norm_all_curves()
    summary_logging(warn, error, critical, 'XRD')
    return xrd_session


if __name__ == '__main__':
    from Unpack.Unpack import package
    a = XRD_pack()
