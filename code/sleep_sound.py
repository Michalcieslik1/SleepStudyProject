#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 20:30:01 2022
@author: veerlemaslowski
@author: Michał Cieślik

Before running, in the terminal:
- test that 'afplay /path/to/sound/' works
-
TODO: Need to pick a read/write file module, threading module
"""
# Native Sound module
# Possible sound modules: https://pythonbasics.org/python-play-sound/
import os                    # For playing sounds
from typing import Final     # Final variables
import random                # Random variables
import json

WAIT_MAX: Final[int] = 30
WAIT_MIN: Final[int] = 15
SEQUENCE_QUEUE_SIZE: Final[int] = 5


# Class that writes to the Json file to save progress of the brainwaves
class Json:
    SAVE_FILE_NAME = ""

    # TODO: Json class
    def __init__(self, filename):
        SAVE_FILE_NAME = filename
        pass

    # @staticmethod function Save() that saves current brainwave data to Json, uses toJson()
    @staticmethod
    def save():
        pass

    # function toJson() that translates the current data into json file
    def toJson(self):
        pass


# Class that stores the brainwave data, JSON-compatible
class Data:
    # TODO: Data class
    def __init__(self):
        pass


class Start:
    # TODO: Write multithreaded code that starts playing the sounds, possibly fixed by combining dreem usable.py
    def __init__(self):
        pass

    # @staticmethod function startLoop() that is the actual loop that checks over the data every n seconds,
    #     and either returns the result or changes the state of the program (TBD)
    @staticmethod
    def startLoop():
        pass


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
        os.system("afplay " + self.soundPath)
        pass


# Creates an Array of Sound objects with random sounds;
class SoundSequence(Json, Start):
    soundPathArray = []
    sequence = []

    def __init__(self, path):
        self.soundPathArray = path
        self.createSoundSequence()
        pass

    # Creates the beginning sound sequence of length SEQUENCE_QUEUE_SIZE
    def createSoundSequence(self):
        while len(self.sequence) < SEQUENCE_QUEUE_SIZE:
            self.sequence.append(self.createSoundObject())
        pass

    # Create a sound object with a random wait time between WAIT_MIN and WAIT_MAX,
    #    and a random sound from soundPathArray
    def createSoundObject(self):
        i = random.randint(0, len(self.soundPathArray) - 1)
        path = self.soundPathArray[i]
        t = random.randint(WAIT_MIN, WAIT_MAX)

        return Sound(path, t)
        pass

    # Returns the next Sound object and adds a new random sound object
    def pop(self):
        self.sequence.append(self.createSoundObject())
        return self.sequence.pop()
        pass


class Main:
    # TODO: main class
    # Create all the objects
    setupArray = ["code/assets/Sound1.wav", "code/assets/Sound2.wav",
                  "code/assets/Sound3.wav"]
    soundSequence = SoundSequence(setupArray)

    # let user choose all the read/writes

    # Start the experiment

    pass


if __name__ == "__Main__":
    Main()
