class KeywordMatch(object):
    def __init__(self, thing, keywords):
        self.thing = thing
        self.keywords = list(keywords)

class CommentKeywordWatcher(object):
    def __init__(self, subreddit):
        self.stream = subreddit.stream.comments(pause_after=0)
        self.keywords = set()

    def add_keyword(self, kw):
        self.keywords.add(kw)

    def rm_keyword(self, kw):
        self.keywords.remove(kw)

    def check(self):
        matches = []

        for thing in self.stream:
            if not thing:
                break

            if not thing.author:
                continue

            if thing.author.name == 'AutoModerator':
                continue

            thing_matches = [kw for kw in self.keywords if kw.lower() in thing.body.lower()]
            if thing_matches:
                matches.append(KeywordMatch(thing, thing_matches))

        return matches
