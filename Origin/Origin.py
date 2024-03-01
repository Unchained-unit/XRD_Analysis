from Logging import debug, info, warn, error, critical

class origin_session():

    def __init__(self):
        try:
            import originpro as op
            debug('it is')
        except:
            pass

