from Logging import debug, info, warn, error, critical

class origin_session():

    def __init__(self):
        try:
            import originpro as op
            debug('[ORIGIN] --> originpro is installed')
            if op.oext:
                op.set_show(True)
            wks_original = op.new_sheet(type='w', lname='XRD_orig')
        except:
            error('[ORIGIN] --> originpro is NOT installed')



