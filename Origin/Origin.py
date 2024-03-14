from Logging import debug, info, warn, error, critical
import originpro as op

class origin_session():

    def __init__(self):
        wks_original = op.new_sheet(type='w', lname='XRD_orig')
        wks_peak_normalize = op.new_sheet(type='w', lname='XRD_orig')
        wks_normalize_FTO = op.new_sheet(type='w', lname='XRD_orig')


    def show(self):
        if op.oext:
            op.set_show(True)



