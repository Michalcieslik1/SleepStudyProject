# SleepStudyProject

## TO_DO:
### Implement the JSON - compatible class Data that saves all of the brain data together with the participant ID, and sounds being used
 - For more details for how the data is being saved currently look at the Mathlab code, lines 390 - 394
 - Currently using fprintf directly into file, abstract it more.
 - Possibly obsolete, Biosemi can save the brainwave data itself, but all of the info about the participant needs to still be saved and associated with the brain data somehow

### Add markers to the loop
- The data is being recorded through Biosemi. Biosemi's data needs to be marked every time:
#### The sleep state changes from the desired sleep state and vice versa
#### A sound is played
