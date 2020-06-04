from datetime import datetime, timedelta

print('Importing utils...')

class Logger(object):

    def __call__(self, *args, **kwargs):
        self.log(*args, **kwargs)

    def log(self, *args, **kwargs):
        print( '{}>'.format(datetime.now().strftime('%H:%M:%S')), *args, **kwargs )


log = Logger()

class Timer(object):

    def __init__(self, msg='', log=Logger()):
        self.start = None
        self.end=None
        self.elapsed=None
        self.msg = msg
        self.log=log

    def __enter__(self):
        self.start = datetime.now()
        self.log('{}...'.format( self.msg ))
        return self

    def __exit__(self, *args):
        self.end = datetime.now()
        self.elapsed = self.end - self.start
        self.log( '{} took {}'.format( self.msg, self.elapsed ) )


class MultiDate:

    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, initDate):

        if isinstance( initDate, str):
            self.dateAsStr = initDate
            self.dateAsDate = self._toDate(initDate)

        elif isinstance( initDate, datetime ):
            self.dateAsDate = initDate
            self.dateAsStr = self._toString( initDate )

    def _toString(self, date):
        return date.strftime(self.DATE_FORMAT)

    def _toDate(self, date):
        return datetime.strptime(date, self.DATE_FORMAT)

    def asStr(self, offset=0):
        return self._toString(self.dateAsDate + timedelta(offset))

    def asDate(self, offset=0):
        return self.dateAsDate + timedelta(offset)

