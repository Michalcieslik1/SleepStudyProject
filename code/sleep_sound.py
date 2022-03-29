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
import threading
import time
import math

WAIT_MAX: Final[int] = 5
WAIT_MIN: Final[int] = 1
SEQUENCE_QUEUE_SIZE: Final[int] = 5


# Class that writes to the Json file to save progress of the brainwaves
class Json:
    SAVE_FILE_NAME = ""

    # TODO: Instead of a JSON class, make this a class that marks when a sound is being played within z3score
    # For reference look at mathlab code.
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
    # TODO: Data class, Most likely not important
    def __init__(self):
        pass


class ThreadLoop(threading.Thread):
    # TODO: Write multithreaded code that starts playing the sounds
    def __init__(self, soundsequence):
        threading.Thread.__init__(self)
        self.ThisSoundSequence = soundsequence
        self.running = False
        self.start_time = 0
        self.current_time = 0
        pass

    # function run() that is the actual loop that plays the pre-made sequence. It runs concurrently
    #       to main.
    def run(self):
        self.running = True
        self.start_time = time.time()

        # pop the first sound object from the sequence
        current_sound = self.ThisSoundSequence.pop()
        while self.running:
            # calculate the amount of time passed from the starting of the iteration and print it out
            t = time.time() - self.start_time
            if math.floor(t) > self.current_time:
                print(str(math.floor(t)) + " seconds")

            # if the time passed corresponds to the sound object's wait time, play the sound, and
            #       reset the start time to be the current time
            if t >= current_sound.getWaitTime():
                print("Sound played! Path to sound: " + current_sound.soundPath)
                current_sound.play()
                current_sound = self.ThisSoundSequence.pop()
                self.start_time = time.time()

            self.current_time = math.floor(t)
            pass
        # TODO: Write functions pause() and resume() in the vein of the following reference: https://topic.alibabacloud.com/a/python-thread-pause-resume-exit-detail-and-example-_python_1_29_20095165.html

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
class SoundSequence:
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
    thread = ThreadLoop(soundSequence)

    # Start the experiment
    thread.start()
    #time.sleep(10)
    #thread.pause()

if __name__ == "__Main__":
    Main()
