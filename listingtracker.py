import datetime

class ListingEvent(object):
    _epoch = datetime.datetime.utcfromtimestamp(0)

    def __init__(self, submission, new_position, prev_position, t=None):
        self.submission = submission
        self.new_position = new_position
        self.prev_position = prev_position
        if t is None:
            t = datetime.datetime.now()
        self.time = t

    def json_obj(self):
        return {
            'type': 'listing',
            'timestamp': (self.time - self._epoch).total_seconds(),
            'id': self.submission.fullname,
            'new_position': self.new_position,
            'prev_position': self.prev_position,
        }

class ListingTracker(object):
    def __init__(self, list_fn, n=25):
        self.list_fn = list_fn
        self.n = n
        self.prev_positions = {}
        self.seen = set()

    def check(self):
        events = []
        next_positions = {}

        seen = set()
        for i,submission in enumerate(self.list_fn(limit=self.n)):
            seen.add(submission.fullname)

            prev_position = self.prev_positions.get(submission.fullname, -1)
            if i != prev_position:
                events.append(ListingEvent(submission, i+1, prev_position+1))

            next_positions[submission.fullname] = i

        for fullname in self.prev_positions:
            if fullname not in seen:
                events.append(ListingEvent(submission, 0, prev_position+1))

        self.prev_positions = next_positions
        return events
