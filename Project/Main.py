from SoundInterface.SoundSequence import *
from ThreadLoop import *
from typing import Final  # Final variables
from SaveData.Json import *

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
WAIT_MAX = 0
WAIT_MIN = 0
SEQUENCE_QUEUE_SIZE: Final[int] = 5


class Main:
    print("-------------------------(" + str(datetime.date.today()) + ")----------------------------")
    print("Welcome to the experiment!")
    PARTICIPANT_NUM = int(input("Please enter the participant Number:"))
    SOUNDS = int(input("Please enter 2 integers corresponding to sounds (TODO): "))
    WAIT_MIN = int(input("Please enter the minimum wait time between sounds:"))
    WAIT_MAX = int(input("Please enter the maximum wait time between sounds:"))

    SAVE_DATA = Json(PARTICIPANT_NUM, SOUNDS, WAIT_MIN, WAIT_MAX)

    # Sounds used in the experiment + setup
    setupArray = ["/Users/michalcieslik/PycharmProjects/SleepStudyProject/Project/assets/Sound1.wav",
                  "/Users/michalcieslik/PycharmProjects/SleepStudyProject/Project/assets/Sound2.wav",
                  "/Users/michalcieslik/PycharmProjects/SleepStudyProject/Project/assets/Sound3.wav"]
    soundSequence = SoundSequence(setupArray, SEQUENCE_QUEUE_SIZE, WAIT_MIN, WAIT_MAX)
    thread = ThreadLoop(soundSequence)

    # Start the experiment
    input("Press enter to start the experiment")
    print("Experiment started!")
    thread.start()
    thread.pause()

    isRunning = False

    while True:
        if not isRunning:
            input("------SoundSequence paused! Press enter to resume-------\n")
            thread.resume()
            isRunning = True
        else:
            input("------SoundSequence is running! Press enter to pause------\n")
            thread.pause()
            isRunning = False
            pass
        pass


if __name__ == "__Main__":
    Main()
