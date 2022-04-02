from SoundInterface.SoundSequence import *
from ThreadLoop import *
from SaveData.Data import *


# This class will be used by dreem usable.py to pause and resume the playing of the SoundSequence object,
#     and send the messages into Biosemi.
class SleepSoundController:
    data = Data()

    def __init__(self, soundPathArray, participantNum):
        self.setupArray = soundPathArray
        self.participantNum = participantNum
        self.soundSequence = SoundSequence(self.setupArray)
        self.thread = ThreadLoop(self.soundSequence)
        pass

    # TODO: Send the marker to Biosemi that the experiment started
    # Code when phase is started = 0
    def startExperiment(self):
        self.thread.start()
        pass

    # TODO: Send the marker to Biosemi that the participant left the N2 stage
    # Code when non-N2 sleep detected = 4
    def pauseExperiment(self):
        self.thread.pause()

    pass

    # TODO: Send the marker to Biosemi that the participant got to the N2 stage
    # Code when non-N2 sleep detected = 4
    def resumeExperiment(self):
        self.thread.resume()

    pass

pass
