from SoundInterface.SoundSequence import *
from ThreadLoop import *
from typing import Final  # Final variables
"""
Created on Wed Feb  9 20:30:01 2022
@author: veerlemaslowski
@author: Michał Cieślik

Before running, in the terminal:
- test that 'afplay /path/to/sound/' works
TODO: Need to pick a read/write file module, threading module
"""
WAIT_MAX: Final[int] = 5
WAIT_MIN: Final[int] = 1
SEQUENCE_QUEUE_SIZE: Final[int] = 5


class Main:
    # Sounds used in the experiment + setup
    setupArray = ["/Users/michalcieslik/PycharmProjects/SleepStudyProject/Project/assets/Sound1.wav", "/Users/michalcieslik/PycharmProjects/SleepStudyProject/Project/assets/Sound2.wav",
                  "/Users/michalcieslik/PycharmProjects/SleepStudyProject/Project/assets/Sound3.wav"]
    soundSequence = SoundSequence(setupArray, SEQUENCE_QUEUE_SIZE, WAIT_MIN, WAIT_MAX)
    thread = ThreadLoop(soundSequence)

    # Start the experiment
    thread.start()


if __name__ == "__Main__":
    Main()
