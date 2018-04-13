import datetime
from baseevent import BaseEvent

class ListingEvent(BaseEvent):
    def __init__(self, submission, new_position, prev_position, t=None):
        BaseEvent.__init__(self, 'listing', submission, new_position, prev_position, t)

class ListingTracker(object):
    def __init__(self, list_fn, n = None):
        if n is None:
            n = 25

        self.list_fn = list_fn
        self.n = n
        self.prev_positions = {}
        self.submissions = {}

    def check(self):
        events = []
        next_positions = {}

        seen = set()
        for i,submission in enumerate(self.list_fn(limit=self.n)):
            self.submissions[submission.fullname] = submission

            seen.add(submission.fullname)

            prev_position = self.prev_positions.get(submission.fullname, -1)
            if i != prev_position:
                events.append(ListingEvent(submission, i+1, prev_position+1))

            next_positions[submission.fullname] = i

        for fullname,prev_position in self.prev_positions.iteritems():
            if fullname not in seen:
                submission = self.submissions[fullname]
                events.append(ListingEvent(submission, 0, prev_position+1))
                del self.submissions[fullname]

        self.prev_positions = next_positions
        return events
