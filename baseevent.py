import datetime

class BaseEvent(object):
    _epoch = datetime.datetime.utcfromtimestamp(0)

    def __init__(self, type, submission, current, previous, t=None):
        self.type = type
        self.submission = submission
        self.current = current
        self.previous = previous
        if t is None:
            t = datetime.datetime.now()
        self.time = t

    def json_obj(self):
        return {
            'type': self.type,
            'timestamp': (self.time - self._epoch).total_seconds(),
            'id': self.submission.fullname,
            'current': self.current,
            'previous': self.previous,
        }

