from SoundInterface.Sound import *
import random


# Creates an Array of Sound objects with random sounds;
class SoundSequence:
    soundPathArray = []
    sequence = []

    def __init__(self, path, queueSize, minWait, maxWait):
        self.soundPathArray = path
        self.queueSize = queueSize
        self.minWait = minWait
        self.maxWait = maxWait

        self.createSoundSequence()
        pass

    # Creates the beginning sound sequence of length SEQUENCE_QUEUE_SIZE
    # TODO: the two sounds need to be played a set amount of times at random time intervals, 15 each
    def createSoundSequence(self):
        while len(self.sequence) < self.queueSize:
            self.sequence.append(self.createSoundObject())
        pass

    # Create a sound object with a random wait time between WAIT_MIN and WAIT_MAX,
    #    and a random sound from soundPathArray
    def createSoundObject(self):
        i = random.randint(0, len(self.soundPathArray) - 1) # Should pick a specific number of souds
        path = self.soundPathArray[i]
        t = random.randint(self.minWait,self.maxWait)

        return Sound(path, t)
        pass

    # Returns the next Sound object and adds a new random sound object
    def pop(self):
        self.sequence.append(self.createSoundObject())
        return self.sequence.pop()
        pass
