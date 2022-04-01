from SoundInterface.SoundSequence import *
from ThreadLoop import *
from typing import Final  # Final variables
import tkinter as tk
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
    pop_up = tk.Tk()

    tk.Label(pop_up, text="Participant Number: ").grid(row=0)
    tk.Label(pop_up, text="Sound Name: ").grid(row=1)

    participantNum = tk.Entry(pop_up)
    soundName = tk.Entry(pop_up)

    participantNum.grid(row=0, column=1)
    soundName.grid(row=1, column=1)

    pop_up.mainloop()

    # Sounds used in the experiment + setup
    setupArray = ["/Users/michalcieslik/PycharmProjects/SleepStudyProject/Project/assets/Sound1.wav", "/Users/michalcieslik/PycharmProjects/SleepStudyProject/Project/assets/Sound2.wav",
                  "/Users/michalcieslik/PycharmProjects/SleepStudyProject/Project/assets/Sound3.wav"]
    soundSequence = SoundSequence(setupArray, SEQUENCE_QUEUE_SIZE, WAIT_MIN, WAIT_MAX)
    thread = ThreadLoop(soundSequence)

    # Start the experiment
    thread.start()


if __name__ == "__Main__":
    Main()
