from SoundInterface.SoundSequence import *
from ThreadLoop import *
from Popup import *
from typing import Final  # Final variables
from SaveData.Json import *
import tkinter as tk
import keyboard
from tkinter import simpledialog

"""
Created on Wed Feb  9 20:30:01 2022
@author: veerlemaslowski
@author: Michał Cieślik

Before running, in the terminal:
- test that 'afplay /path/to/sound/' works
TODO: Need to pick a read/write file module, threading module

Tkinter tutorial: https://realpython.com/python-gui-tkinter/#getting-multiline-user-input-with-text-widgets
"""
WAIT_MAX = 0
WAIT_MIN = 0
SEQUENCE_QUEUE_SIZE: Final[int] = 5


class Main:
    # Handling of user input
    root = tk.Tk()
    ents = makeForm(root, fields)
    b2 = tk.Button(root, text='Quit', command=root.quit)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()

    # Saving of the user input in a Json class
    WAIT_MIN = int(ents[2][1].get())
    WAIT_MAX = int(ents[3][1].get())

    SAVE_DATA = Json(ents[1][1].get(), ents[0][1].get(), WAIT_MIN, WAIT_MAX)

    # Sounds used in the experiment + setup
    setupArray = ["/Users/michalcieslik/PycharmProjects/SleepStudyProject/Project/assets/Sound1.wav",
                  "/Users/michalcieslik/PycharmProjects/SleepStudyProject/Project/assets/Sound2.wav",
                  "/Users/michalcieslik/PycharmProjects/SleepStudyProject/Project/assets/Sound3.wav"]
    soundSequence = SoundSequence(setupArray, SEQUENCE_QUEUE_SIZE, WAIT_MIN, WAIT_MAX)
    thread = ThreadLoop(soundSequence)

    # Start the experiment
    thread.start()

    pass


if __name__ == "__Main__":
    Main()
