class Scorer(object):
    def __init__(self, r, smooth_count = 5):
        self.r = r
        self.smooth_count = smooth_count

    def score(self, submissions):
        scores = dict([(submission['fullname'], 0) for submission in submissions])

        for i in range(self.smooth_count):
            for info in self.r.info(fullnames=[submission['fullname'] for submission in submissions]):
                scores[info.fullname] += info.score

        for id in scores.keys():
            scores[id] /= float(self.smooth_count)

        return scores
