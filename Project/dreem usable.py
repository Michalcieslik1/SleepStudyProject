#
# Script running during the Dreem experiment
# Start when the EEG rig and ActiView are up and running
# Collects data from ActiView; connects to Z3Score and scores sleep
#
# Written by Rayo Verweij, hit me up if you have a question
# Using elements of pyactivetwo by Ilya Kuzovkin
# And connects to Z3Score by Neurobit Technologies Pte Ltd Singapore
# Special thanks to Zongheng Zhang for patiently sitting with electrodes
# on his face while I was testing things
#
# Tested on Python 3.7 on Windows
# Requires these Python libraries:
# pycfslib, pyedflib, pygame, pebble, pyqtgraph
# pillow, PyQt5, requests, socket, numpy, and scipy
#
# [(－－)]..zzZ
#

import os
import math
import csv
import socket  # For connecting to ActiView
import numpy as np
import scipy.signal as scisig  # Used in DC block
from requests import post  # For connecting to Z3
from time import time, sleep  # Time access & thread sleeping
import multiprocessing as mp  # Multiprocessing used bc plotting is CPU intensive
from pebble import ProcessPool  # Allows for cancelling processes, mp doesn't
from pycfslib import create_stream_v2 as stream_data  # To encode channel data in Z3's CFS format before sending
from SleepSoundController import *

######################################################################
##### INITIALIZATION
######################################################################
# Login info for Z3Score
server_url = 'https://z3score.com/api/v2'
email = 'jhulbert@bard.edu'
key = 'O%2FRe%2BvrWLOpl7VqM9XBHiS2THTrx%2B%2BMcC6BOIKZHHQQ%3D'

# Connecting to ActiView; address is 127.0.0.1 if running on the same PC
TCP_IP = '10.20.40.135'

# The port that ActiView listens to
TCP_PORT = 778

# The number of channels we use
NUM_CHANNELS = 40

# The number of samples retrieved with every call to ActiView (depends on ActiView's settings)
SAMPLES = 16

# Data packet size
BUFFER_SIZE = NUM_CHANNELS * SAMPLES * 3

# Sampling rate
SAMPLING_RATE = 512

# Score every 3 seconds
SCORING_FREQUENCY = 3

# Update the real-time plot every 50 ms. Note that plotting is CPU intensive
PLOT_UPDATE_TIME = 50

# Codes for sleep stages
stage_keys = {
    0: 'Wake',
    1: 'NREM 1',
    2: 'NREM 2',
    3: 'NREM 3',
    5: 'REM',
    9: 'Unknown',
}


######################################################################
##### GENERATE AUTH TOKEN
######################################################################
# Requesting an auth token from Z3 means we don't have to log in
# every time we send data, making the process much faster
# The token expires after 16 hours
# https://github.com/neurobittechnologies/realtime-sleep-staging
def request_token():
    # Try to contact the server
    try:
        # Requests.post() ==> sends data to a specified server. Returns requests.Response object
        response = post(server_url + '/get-token', data={'email': email, 'key': key})
    except:
        print("There was an error communicating with Z3.")
        exit(0)

    # status Project 200 means OK, 404 means not found.
    if response.status_code != 200:
        print("There was an error communicating with Z3.")
        exit(0)

    # returns a JSON object of the result of the response
    data = response.json()
    token = data['token']

    # Check if the token has been generated
    if data['token'] == 0:
        print("Could not generate token to access Z3.")
        print(data['message'])
        exit(0)

    print("Successfully connected to the real-time scoring module of Z3.")
    return token


######################################################################
##### STAGE SLEEP DATA
######################################################################
# Takes the channel data, sends it to Z3, and return the stage
# sampling_rates is a lit of size 5 with sampling rates of the channels
# token is the authorization token generated in the function above
def process_and_stage(C3, C4, EOGL, EOGR, EMG, sampling_rates, token):
    ## Compress the channel data to Z3's CFS format using pycfslib
    stream = stream_data(C3, C4, EOGL, EOGR, EMG, sampling_rates)
    ## make file conform to JSON
    files = {'file': ('stream.cfs', stream)}

    ## Contact the server
    try:
        response = post(server_url + '/realtime', files=files, data={'token': token})
    except:
        print("There was an error communicating with Z3.")
        return [9, 10]

    if response.status_code != 200:
        print("There was an error communicating with Z3.")
        stage = [9, 10]
    else:
        data = response.json()
        if data['status'] == 0:
            print("Scoring failed...\n")
            print(data['message'])
            stage = [9, 10]
        else:
            stage = data['message']

    return stage


######################################################################
##### MAIN FUNCTION
######################################################################
if __name__ == "__main__":
    print("It's so good to see you again!")

    ## Set up the SleepSoundController class
    soundController = SleepSoundController()

    ## Request an auth token
    token = request_token()

    ## Open socket to ActiView
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    print("Successfully connected to ActiView.")

    ## Initializing data structures
    # The module requires 60 seconds of data, so the running window is exactly 60 seconds long
    window_length = 60 * SAMPLING_RATE
    running_window = np.zeros((5, window_length))
    blank_data = np.zeros((window_length))

    sleep_stages = []
    samples_read = 0

    ## Manage threads
    executor = ProcessPool(max_workers=2)

    ## Data acquisition
    responses = []
    stage = [9, 10]
    last_call_success = False
    last_updated_time = time()

    # This loop *must* run fast enough that all operations are completed before the buffer fills up
    while True:
        # Create a signal buffer of 16 samples for all 40 channels
        signal_buffer = np.zeros((NUM_CHANNELS, 16))

        # Read the next packet from the network
        data = s.recv(BUFFER_SIZE)

        # Extract samples
        for i in range(SAMPLES):
            for ch in range(NUM_CHANNELS):
                offset = i * 3 * NUM_CHANNELS + (ch * 3)  # where does the (ch * 3) come from?
                # The 3 bytes of each sample arrive in reverse order (= little-endian)
                try:
                    sample = (data[offset + 2] << 16)  # 8454144
                except IndexError as error:
                    print("Error: " + str(error) + " - don't worry, scoring will resume shortly.")
                    continue
                sample += (data[offset + 1] << 8)  # roughly between 63-91
                sample += data[offset]  # roughly between 3-250 (0-256?)
                # sample /= 1000
                # sample -= 8400
                # Store sample in signal buffer
                signal_buffer[ch, i] = sample

        samples_read += SAMPLES

        # Take only the channels we need
        data = np.zeros((5, 16))
        for i in range(SAMPLES):
            data[0, i] = signal_buffer[7, i] - signal_buffer[37, i]  # C3-EX6: ~-6500
            data[1, i] = signal_buffer[22, i] - signal_buffer[36, i]  # C4-EX5: ~-1900
            data[2, i] = signal_buffer[32, i] - signal_buffer[37, i]  # EX1-EX6: ~-2500
            data[3, i] = signal_buffer[33, i] - signal_buffer[36, i]  # EX2-EX5: ~-1500
            data[4, i] = signal_buffer[38, i] - signal_buffer[39, i]  # EX7-EX8: ~-800

        # Position within the second we're reading from; goes from 0 += 0.03125
        t_now = samples_read / SAMPLING_RATE

        # Push new data into running_window and remove old data
        # Fills 'from the back' and after a minute all 0s are replaced with values
        running_window[:, 0:window_length - SAMPLES] = running_window[:, SAMPLES:]
        running_window[:, window_length - SAMPLES:] = data

        # If first call to the server, initialize the schedule for staging
        if not responses:
            print("Initiating first call to Z3.")
            latency = 0
            last_staging_request_time = time()
            t_stage = t_now
            responses.append(executor.schedule(process_and_stage,
                                               (running_window[0, :], running_window[1, :], running_window[2, :],
                                                running_window[3, :], running_window[4, :], np.ones(5) * SAMPLING_RATE,
                                                token),
                                               timeout=SCORING_FREQUENCY))
            print("First call was successful.")

        # Getting back the results from Z3
        if responses[-1].done() and not last_call_success:
            print("Scoring...")
            stage = responses[-1].result()  # looks like [stage, confidence]
            sleep_stages.append([t_stage, stage_keys[stage[0]], stage[1]])
            print("Time: %0.2f. Stage: %s. Confidence: %0.2f." % (t_stage, stage_keys[stage[0]], stage[1]))
            # TODO: Here is where our new code would take in the stage and act accordingly.
            latency = (time() - last_staging_request_time) * 1000  # usually around 100-200
            last_call_success = True

        # If last request did not complete in time, cancel the request and make a new one
        if time() - last_staging_request_time > SCORING_FREQUENCY:
            if not responses[-1].done():
                responses[-1].cancel()
                print("Warning: scoring could not be completed in time.")
                print("Try reducing the SCORING_FREQUENCY.")
                latency = (time() - last_staging_request_time) * 1000
                stage = [9, 10]
                sleep_stages.append([t_stage, stage_keys[stage[0]], stage[1]])
                print("Time: %0.2f. Stage: %s. Confidence: %0.2f." % (t_stage, stage_keys[stage[0]], stage[1]))
                # TODO: Here is also where our new code would take in the stage and act accordingly.

            last_staging_request_time = time()
            t_stage = t_now
            responses.append(executor.schedule(process_and_stage,
                                               (running_window[0, :], running_window[1, :], running_window[2, :],
                                                running_window[3, :], running_window[4, :], np.ones(5) * SAMPLING_RATE,
                                                token),
                                               timeout=SCORING_FREQUENCY))
            last_call_success = False
