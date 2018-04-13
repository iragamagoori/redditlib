def score(r, fullnames, smooth_count = 5):
    scores = dict([(fullname, 0) for fullname in fullnames])

    if fullnames:
        for i in range(smooth_count):
            for info in r.info(fullnames=fullnames):
                scores[info.fullname] += info.score

    for id in scores.keys():
        scores[id] /= float(smooth_count)

    return scores
