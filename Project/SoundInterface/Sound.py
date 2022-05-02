import os
import winsound


# Houses the Sound that is supposed to be played
class Sound:
    soundPath = ""
    waitTime = 0

    def __init__(self, path, t):
        self.soundPath = path
        self.waitTime = t
        pass

    # Gets the time /------/
    def getWaitTime(self):
        return self.waitTime
        pass

    # Plays the specific sound housed in the sound object
    # WARNING: afplay only works on mac. Find an alternative for Windows!
    def play(self):
        #os.system("afplay " + self.soundPath)
        winsound.PlaySound(self.soundPath, winsound.SND_FILENAME|winsound.SND_NOSTOP)
        pass