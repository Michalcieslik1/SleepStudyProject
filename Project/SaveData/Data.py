import datetime
import json


# Class that stores the brainwave data, JSON-compatible
class Data(dict):
    subjectNum = ""
    soundArray = []
    date = ""

    def __init__(self):
        self.subjectNum = ""
        self.soundArray = []
        self.date = datetime.date
        dict.__init__(self)
        pass
    # TODO: Data class, Most likely not important

pass
