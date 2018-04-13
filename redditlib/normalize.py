def normalize_subreddit(subreddit):
    if subreddit.startswith('/r/'):
        return subreddit[3:]

    elif subreddit.startswith('r/'):
        return subreddit[2:]

    else:
        return subreddit

def normalize_username(username):
    if username.startswith('/u/'):
        return username[3:]

    elif username.startswith('u/'):
        return username[2:]

    else:
        return username

def normalize(thing):
    if thing.startswith('/u/') or thing.startswith('/r/'):
        return thing[3:]
    
    elif thing.startswith('u/') or thing.startswith('r/'):
        return thing[2:]

    else:
        return thing
