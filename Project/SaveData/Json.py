import json
import datetime


# Class that writes to the Json file to save progress of the brainwaves
class Json:
    SAVE_FILE_NAME = ""
    subjectNum = ""
    soundArray = []
    date = ""

    # TODO: Instead of a JSON class, make this a class that marks when a sound is being played within z3score
    # For reference look at mathlab Project.
    def __init__(self, subjectNum, soundArray, min, max):
        self.SAVE_FILE_NAME = "SAVE_DATA.txt"

        self.JSONDict = {
            'Subject Number': subjectNum,
            'Sounds': soundArray,
            'Date': str(datetime.date.today()),
            'Min Wait Time': min,
            'Max Wait Time': max,
            'Brain Wave Data': {}
        }

        self.save()
        pass

    # function that saves the info from Data class to file SAVE_FILE_NAME
    def save(self):
        JSONstring = json.dumps(dict(self.JSONDict))
        print("JSON result: " + JSONstring)
        file = open(self.SAVE_FILE_NAME, "w")
        file.write(JSONstring)
        file.close()
        pass

    def update(self, brainWaveData):
        self.JSONDict['Brain Wave Data'].update(brainWaveData)
        self.JSONDict.save()
        pass
