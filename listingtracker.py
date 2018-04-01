class ListingTracker(object):
    def __init__(self, list_fn):
        self.list_fn = list_fn
        self.seen = set()

    def check(self):
        new_submissions = []

        for i,submission in enumerate(self.list_fn(limit=25)):
            if submission.fullname not in self.seen:
                new_submissions.append((i, submission))
                self.seen.add(submission.fullname)

        return new_submissions
