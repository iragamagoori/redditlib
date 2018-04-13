import json

class JsonLog(object):
    def __init__(self, filename, append=False):
        if append:
            mode = 'a'
        else:
            mode = 'w'

        self.f = open(filename, mode)

    def write(self, entry):
        json.dump(entry, self.f)
        self.f.write('\n')
        self.f.flush()
