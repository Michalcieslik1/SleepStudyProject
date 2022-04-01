import json


# Class that writes to the Json file to save progress of the brainwaves
class Json:
    SAVE_FILE_NAME = ""

    # TODO: Instead of a JSON class, make this a class that marks when a sound is being played within z3score
    # For reference look at mathlab Project.
    def __init__(self, filename):
        SAVE_FILE_NAME = filename
        pass

    # function that saves the info from Data class to file SAVE_FILE_NAME
    def save(self, data):
        JSONstring = json.dumps(data)
        file = open(self.SAVE_FILE_NAME, "w")
        file.write(JSONstring)
        file.close()
        pass

