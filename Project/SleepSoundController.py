from SoundInterface.SoundSequence import *
from ThreadLoop import *
from datetime import *
from SaveData.Json import *
from dreem_usable import stage_keys

WAIT_MAX = 0
WAIT_MIN = 0
SEQUENCE_QUEUE_SIZE = 5
# This class will be used by dreem_usable.py to pause and resume the playing of the SoundSequence object,
#     and send the messages into Biosemi.
class SleepSoundController:

    def __init__(self):
        print("-------------------------(" + str(datetime.date.today()) + ")----------------------------")
        print("Welcome to the experiment!")
        self.participantNum = int(input("Please enter the participant Number:"))
        sounds = int(input("Please enter 2 integers corresponding to sounds (TODO): "))
        WAIT_MIN = int(input("Please enter the minimum wait time between sounds:"))
        WAIT_MAX = int(input("Please enter the maximum wait time between sounds:"))

        self.isRunning = False
        self.started = False

        self.SAVE_DATA = Json(self.participantNum, sounds, WAIT_MIN, WAIT_MAX)

        # Sounds used in the experiment + setup
        self.setupArray = ["Project/assets/Sound1.wav",
                           "Project/assets/Sound2.wav",
                           "Project/assets/Sound3.wav"]
        self.soundSequence = SoundSequence(self.setupArray, SEQUENCE_QUEUE_SIZE, WAIT_MIN, WAIT_MAX)
        self.thread = ThreadLoop(self.soundSequence)
        pass

    # Take in the sleep state and pause or restart the soundSequence
    def analyzeSleepState(self, sleepStage):
        if sleepStage == stage_keys[0]: # WARNING: Currently set up so that the sound plays when one is awake
            if not self.isRunning:
                if not self.started:
                    self.startExperiment()
                else:
                    self.resumeExperiment()
                    pass
        else:
            if self.isRunning:
                self.pauseExperiment()
        pass

    # TODO: Send the marker to Biosemi that the experiment started
    # Code when phase is started = 0
    def startExperiment(self):
        print("Experiment started!")
        self.thread.start()
        self.isRunning = True
        self.started = True
        pass

    # TODO: Send the marker to Biosemi that the participant left the N2 stage
    # Code when non-N2 sleep detected = 4
    def pauseExperiment(self):
        self.thread.pause()
        self.isRunning = False
    pass

    # TODO: Send the marker to Biosemi that the participant got to the N2 stage
    # Code when N2 sleep detected = 4
    def resumeExperiment(self):
        self.thread.resume()
        self.isRunning = True
    pass

    def stopExperiment(self):
        self.thread.stop()
        self.isRunning = False
        pass

pass
