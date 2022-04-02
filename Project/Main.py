from SoundInterface.SoundSequence import *
from ThreadLoop import *
from Popup import *
from typing import Final  # Final variables
from SaveData.Json import *
import tkinter as tk
from SaveData.Data import *
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
WAIT_MAX: Final[int] = 5
WAIT_MIN: Final[int] = 1
SEQUENCE_QUEUE_SIZE: Final[int] = 5


class Main:
    # Pop up handling TODO: Finish the Pop up interface
    root = tk.Tk()
    ents = makeForm(root, fields)
    # root.bind('<Return>', (lambda event, e=ents: fetch(e)))
    b2 = tk.Button(root, text='Quit', command=root.quit)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()

    DATA = Data()
    DATA.soundArray = ents[1][1].get()
    DATA.subjectNum = ents[0][1].get()

    saveData = Json(DATA)

    # Sounds used in the experiment + setup
    setupArray = ["/Users/michalcieslik/PycharmProjects/SleepStudyProject/Project/assets/Sound1.wav",
                  "/Users/michalcieslik/PycharmProjects/SleepStudyProject/Project/assets/Sound2.wav",
                  "/Users/michalcieslik/PycharmProjects/SleepStudyProject/Project/assets/Sound3.wav"]
    soundSequence = SoundSequence(setupArray, SEQUENCE_QUEUE_SIZE, WAIT_MIN, WAIT_MAX)
    thread = ThreadLoop(soundSequence)

    # Start the experiment
    thread.start()


if __name__ == "__Main__":
    Main()
