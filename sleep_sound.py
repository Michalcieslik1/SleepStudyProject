#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 20:30:01 2022
@author: veerlemaslowski
TODO: Need to pick a sound module, a read/write file module, threading module
"""


# Class that writes to the Json file to save progress of the brainwaves
class WriteJson:
    # TODO: WriteJson class
    def __init__(self):
        pass

    # @staticmethod function Save() that saves current brainwave data to Json, uses toJson()
    @staticmethod
    def save():
        pass

    # function toJson() that translates the current data into json file
    def toJson(self):
        pass


class Start:
    # TODO: Start the loop class
    def __init__(self):
        pass

    # @staticmethod function startLoop() that is the actual loop that checks over the data every n seconds,
    #     and either returns the result or changes the state of the program (TBD)
    @staticmethod
    def startLoop():
        pass


# Houses the Sound that is supposed to be played
class Sound:
    # TODO: Sound class
    def __init__(self):
        pass

    # Returns the sound that's stored in the class
    def getSound(self):
        pass

    # Plays the specific sound housed in the sound object
    def playSound(self):
        pass


# Creates an Array of Sound objects with random sounds;
class SoundSequence(WriteJson, Start):
    # TODO: SoundSequence class
    def __init__(self):
        super().__init__()

    # Function Start() that starts playing the sequence
    def start(self):
        pass

    # Function that saves the data into the buffer, starts playing sounds if in stage 2


class Main:
    # TODO: main class
    # Create all the objects

    # let user choose all the read/writes

    # Start the experiment

    pass


if __name__ == "__Main__":
    Main()
