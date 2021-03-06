# SleepStudyProject

## TO_DO:
### Implement the JSON - compatible class Data that saves all of the brain data together with the participant ID, and sounds being used
 - For more details for how the data is being saved currently look at the Mathlab code, lines 390 - 394
 - Currently using fprintf directly into file, abstract it more so it uses JSON.
 - Biosemi can save the brainwave data itself, but all of the info about the participant needs to still be saved and associated with the brain data somehow.

### Add markers to the loop
The data is being recorded through Biosemi. Biosemi's data needs to be marked every time:
- A new file is started
- The sleep state changes from the desired sleep state and vice versa
- A sound is played
The marking should be handled through triggers, more info here: https://discourse.psychopy.org/t/sending-markers-to-eeg-through-serial-port/5311, as well as in the original Mathlab code. One example can be found around lines 222:
``` 
if BioSemi %zero out all the parallel port pins before beginning
    s = daq.createSession('ni'); %set up the session--initialize session-based interface to NI-DAQ device for triggering
    ch = addDigitalChannel(s,'Dev1','Port1/Line0:7','OutputOnly'); %Set up an 8-bit range as a channel to which events can be written
    outputSingleScan(s,[0 0 0 0 0 0 0 0]) %reset port to zero, see timing requirement above
end
```
The line that defines s opens the port that our codes are going to be sent through. The actual code being sent happens in the following code:
```
 %send a trigger code (8) indicating the start of the nap phase
    n_start = GetSecs; %log start time for output file (all trigger times in text output will be relative to this)
    trig_time = n_start; %relative trigger time (same as above for this first instance only)
    trig_code = fliplr((dec2bin(8,8))) - '0'; %turn the first input to (flipped) 8-bit binary vector (the string to vector conversion happens with -'0')
    outputSingleScan(s,trig_code)
    WaitSecs(0.004) %pulse on for 4 milliseconds; must be >than time resolution of hardware [try (1000/<EEG sampling rate>)+2ms]
    outputSingleScan(s,[0 0 0 0 0 0 0 0]) %reset port to zero, see timing requirement above
```

#### Biosemi Codes:
- Phase start = 0
- Sound 1 played = 1
- Sound 2 played = 2
- N2 detected = 3
- Non - N2 sleep detected = 4
- Phase end = 9

#### Markers are handled through signals sent through ports. 

One way of doing it is through the package PsychoPy: https://discourse.psychopy.org/t/using-biosemi-usb-trigger-interface-for-sending-triggers/4605
http://psychtoolbox.org/docs/ReceivingTriggerFromSerialPortDemo
https://www.psychopy.org/
https://www.psychtoolbox.net/

Can we just use regular ports?
https://pyserial.readthedocs.io/en/latest/pyserial_api.html
