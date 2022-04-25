from SleepSoundController import *
"""
Created on Wed Feb  9 20:30:01 2022
@author: veerlemaslowski
@author: Michał Cieślik

Before running, in the terminal:
- test that 'afplay /path/to/sound/' works
- install the following modules:
    - Popup
    - Typing
    - tkinter
    - keyboard
TODO: Need to pick a read/write file module, threading module

Tkinter tutorial: https://realpython.com/python-gui-tkinter/#getting-multiline-user-input-with-text-widgets
"""

class Main:
    controller = SleepSoundController()
    controller.startExperiment()
    pass


if __name__ == "__Main__":
    Main()
