import datetime
from baseevent import BaseEvent
from listingtracker import ListingTracker
from scoretracker import ScoreTracker

class SubredditEvent(BaseEvent):
    def __init__(self, event, listing):
        BaseEvent.__init__(self, event.type, event.submission, event.current, event.previous)
        self.listing = listing
        
    def json_obj(self):
        j = BaseEvent.json_obj(self)
        j['listing'] = self.listing
        return j

class SubredditTracker(object):
    def __init__(self, r, subreddit, track_time = None, listing_count = None, smooth_count = None):
        if track_time is None:
            track_time = datetime.timedelta(days = 7)
        
        self.subreddit = subreddit

        self.listing_count = listing_count
        self.hot_tracker = ListingTracker(subreddit.hot, n = listing_count)
        self.rising_tracker = ListingTracker(subreddit.rising, n = listing_count)
        self.new_tracker = ListingTracker(subreddit.new, n = listing_count)
        self.score_tracker = ScoreTracker(r, smooth_count = smooth_count)

        self.track_time = track_time

        self.tracking_queue = []
        self.tracking_lookup = set()

        self.first = False

    def check(self):
        events = []

        events += [SubredditEvent(event, 'hot') for event in self.hot_tracker.check()]
        events += [SubredditEvent(event, 'rising') for event in self.rising_tracker.check()]

        new_submissions = []

        new_events = self.new_tracker.check()
        for event in new_events:
            submission = event.submission

            if event.current == self.listing_count:
                if submission.id not in self.tracking_lookup and not self.first:
                    print >>sys.stderr, 'WARNING:'
                    print >>sys.stderr, '    Oldest entry in new not previously seen.'
                    print >>sys.stderr, '    Some submissions might slip through the cracks and not get tracked.'

            if event.age < self.track_time and submission.id not in self.tracking_lookup:
                self.tracking_queue.append(submission)
                self.tracking_lookup.add(submission.id)
                new_submissions.append(submission)

            events.append(SubredditEvent(event, 'new'))

        self.score_tracker.add(new_submissions)

        i = 0
        new_head = []
        for submission in self.tracking_queue[:self.listing_count]:
            t_now = datetime.datetime.now()
            t_created = datetime.datetime.fromtimestamp(submission.created_utc)

            if t_now - t_created <= self.track_time:
                new_head.append(submission)
            else:
                self.tracking_lookup.remove(submission.id)
                self.score_tracker.remove(submission)

        events += self.score_tracker.check()

        self.tracking_queue = new_head + self.tracking_queue[self.listing_count:]

        self.first = False

        return events
