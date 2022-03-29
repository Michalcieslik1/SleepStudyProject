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
The marking should be handled through triggers, more info here: https://discourse.psychopy.org/t/sending-markers-to-eeg-through-serial-port/5311, as well as in the original Mathlab code

## Biosemi Codes:
- Phase start = 0
- Sound 1 played = 1
- Sound 2 played = 2
- N2 detected = 3
- Non - N2 sleep detected = 4
- Phase end = 9
