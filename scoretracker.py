import praw

import datetime
from baseevent import BaseEvent
from score import score

class ScoreEvent(BaseEvent):
    def __init__(self, submission, new_score, prev_score, t=None):
        BaseEvent.__init__(self, 'score', submission, new_score, prev_score, t)

class ScoreTracker(object):
    def __init__(self, r, smooth_count = None):
        if smooth_count is None:
            smooth_count = 5

        self.r = r
        self.smooth_count = smooth_count
        self.scores = {}
        self.submissions = {}

    def add(self, submissions):
        if isinstance(submissions, praw.models.Submission):
            submissions = [submissions]

        if not submissions:
            return

        scores = score(self.r, [submission.fullname for submission in submissions], self.smooth_count)
        self.scores.update(scores)

        self.submissions.update(dict([(submission.fullname, submission) for submission in submissions]))

    def remove(self, submissions):
        if isinstance(submissions, praw.models.Submission):
            submissions = [submissions]

        for submission in submissions:
            self.scores.pop(submission.fullname, None)
            self.submissions.pop(submission.fullname, None)

    def check(self):
        events = []
        next_scores = score(self.r, self.scores.keys(), self.smooth_count)

        for fullname, prev_score in self.scores.iteritems():
            next_score = next_scores.get(fullname, 0)
            if prev_score != next_score:
                events.append(ScoreEvent(self.submissions[fullname], next_score, prev_score))

        self.scores = next_scores
        return events
