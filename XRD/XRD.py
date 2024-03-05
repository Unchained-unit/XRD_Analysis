from Logging.Logging import debug, info, warn, error, critical
from Unpack.Unpack import package

class XRD_pattern():

    x_values = []
    y_values = []
    def __init__(self, xrd_dict):
        for keys, values in xrd_dict.items():
            self.x_values.append(keys)
            self.y_values.append(values)
        debug('[XRD] --> x and y values are formed')

    def peaks(self):
        pass
class XRD_pack():

    def __init__(self, xrds):
        self.xrds_pack = [XRD_pattern(xrd) for xrd in xrds]
        debug('[XRD] --> XRD_pack is formed')


if __name__ == '__main__':
    from Unpack.Unpack import package
    a = XRD_pack()
