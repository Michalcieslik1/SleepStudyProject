import Project
import threading
import time
import math


# The loop that plays out the SoundSequences, with pause, resume, and stop functionality
class ThreadLoop(threading.Thread):
    # TODO: Write multithreaded Project that starts playing the sounds
    def __init__(self, soundsequence):
        threading.Thread.__init__(self)
        self.__flag = threading.Event()  # Flag used to pause the thread
        self.__flag.set()  # Set flag to true
        self.__running = threading.Event()
        self.__running.set()

        self.ThisSoundSequence = soundsequence
        self.start_time = 0
        self.current_time = 0
        pass

    # function run() that is the actual loop that plays the pre-made sequence. It runs concurrently
    #       to main.
    def run(self):
        self.start_time = time.time()

        # pop the first sound object from the sequence
        current_sound = self.ThisSoundSequence.pop()
        while self.__running.is_set():
            self.__flag.wait()
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
    def pause(self):
        self.__flag.clear()  # Set to False to block the thread

    def resume(self):
        self.__flag.set()  # Set to True, let the thread stop blocking

    def stop(self):
        self.__flag.set()  # Resume the thread from the suspended state, if it is already suspended
        self.__running.clear()  # Set to False

