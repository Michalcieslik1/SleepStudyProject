function Sleep_stage()

%Sleep_stage.m Allows the experimenter to manually identify N2 sleep, which
%starts a 60-second countdown clock, which can be interrupted at any time
%should they detect an arousal or a transition to another sleep stage. Once
%the timer has elapsed, two pre-specified sounds will play a total of 15
%times each, in block randomized order (so that they will be played in
%pairs) with jittered ISIs. Trigger codes can be sent over the BioSemi
%system to the EEG recording computer. Created by Zongheng Zhang.

%Recall the word lists after sleep/wake delay

%% script version
VERSION_NO = '1.00';

% Figure out which computer is being used
try %my computer
    cd('C:\Users\EEGstim\Desktop\Dreem_Rrr');
    WORKING_DIR = 'C:\Users\EEGstim\Desktop\Dreem_Rrr';
    
catch
    cd('~/Desktop/Dreem_Rrr/');
    WORKING_DIR = '~/Desktop/Dreem_Rrr/';
end
cd(WORKING_DIR)

% Check we're in the right directory
assert(logical(exist('./stimuli','dir')),...
    sprintf('(*) "stimuli" directory does not exisit in: %s',pwd));

% Set the key code for the OS
if ismac
    return_key = 40;
elseif isunix
    return_key = 37;
elseif ispc
    return_key = 13;
end

%% Collect subject information & prepare stim/output files

prompt = {'Enter subject number:','DFcond','Tcond','Version','SoundFile1','SoundFile2'}; %description of fields
defaults = {'','A|B','1|2','E|C','1-6','1-6'}; %default response options
answer = inputdlg(prompt, 'Subject Number',1.6,defaults); %opens dialogue
SUBJECT = answer{1,:}; %Extract Subject Number
DFcond = answer{2,:}; %Indicates whether the first block is Forget (1) or Remember (2)--the second block is the opposite
Tcond = answer{3,:}; %Indicates whether the 2nd list from Block 1 or Block 2 is tested first in the final phase
Version = answer{4,:}; %Indicates whether [E]xperimental (sound replays) or [C]ontrol (novel sounds)
SoundFile1 = answer{5,:}; %Indicates one of the two soudns to be played during the nap (repeated or control, depending on Version)--this information should've been recorded by the experimenter in the study phase as Nap_sounds/"np files #"
SoundFile2 = answer{6,:}; %Indicates one of the two soudns to be played during the nap (repeated or control, depending on Version)--this information should've been recorded by the experimenter in the study phase as Nap_sounds/"np files #"
c = clock; %Current date and time as date vector. [year month day hour minute seconds]

% This erases any spaces in the inputs
SUBJECT = strrep(SUBJECT,' ','');
DFcond = strrep(DFcond,' ','');
Tcond = strrep(Tcond,' ','');
Version = strrep(Version,' ','');
SoundFile1 = strrep(SoundFile1,' ','');
SoundFile2 = strrep(SoundFile2,' ','');

% Prompts experimenter to double-check subject information - make experimenter
% enter data in TWICE and checks those against eachother
prompt2 = {'Enter subject number:','DFcond','Tcond','Version'}; %description of fields
answer2 = inputdlg(prompt, 'Subject Number',1.6,defaults); %opens dialogue
SUBJECT2 = answer2{1,:}; %Extract Subject Number
DFcond2 = answer2{2,:}; %Indicates whether the first block is Forget (1) or Remember (2)--the second block is the opposite
Tcond2 = answer2{3,:}; %Indicates whether the 2nd list from Block 1 or Block 2 is tested first in the final phase
Version2 = answer2{4,:}; %Indicates whether [E]xperimental (sound replays) or [C]ontrol (novel sounds)
SoundFile1_2 = answer2{5,:}; %Indicates one of the two soudns to be played during the nap (repeated or control, depending on Version)--this information should've been recorded by the experimenter in the study phase as Nap_sounds/"np files #"
SoundFile2_2 = answer2{6,:}; %Indicates one of the two soudns to be played during the nap (repeated or control, depending on Version)--this information should've been recorded by the experimenter in the study phase as Nap_sounds/"np files #"

% This erases any spaces in the inputs
SUBJECT2 = strrep(SUBJECT2,' ','');
DFcond2 = strrep(DFcond2,' ','');
Tcond2 = strrep(Tcond2,' ','');
Version2 = strrep(Version2,' ','');
SoundFile1 = strrep(SoundFile1_2,' ','');
SoundFile2 = strrep(SoundFile2_2,' ','');

% Creates arrays for both inputs
aarray = [SUBJECT, DFcond, Tcond, Version, SoundFile1, SoundFile2];
barray = [SUBJECT2, DFcond2, Tcond2, Version2, SoundFile1_2, SoundFile2_2];

% Check if the arrays are equal
doublecheck = isequal(aarray,barray);
try
    assert(isequal(doublecheck,1), 'Invalid participant information. Please enter again.');
catch
    %Error. Close screen, show cursor, rethrow error:
    ShowCursor;
    Screen('CloseAll');
    %clc; %clear command window
    fclose('all');
    Priority(0);
    psychethrow(psychlasterror);
end

%convert to numbers
Tcond = str2num(Tcond);
SoundFile1 = str2num(SoundFile1);
SoundFile2 = str2num(SoundFile2);
if DFcond == 'a'|| DFcond == 'A'
    DFcond = 1;
elseif DFcond == 'b' || DFcond == 'B'
    DFcond = 2;
end

baseName=[SUBJECT '_DFcond_' num2str(DFcond) '_Tcond_' num2str(Tcond) '_Version_' Version '_NapSoundFile1-' num2str(SoundFile1) '_NapSoundFile2-' num2str(SoundFile2) '_' mfilename() '_' num2str(c(2)) '_' num2str(c(3)) '_' num2str(c(4)) '_' mfilename(5) '_' num2str(c(6))]; %makes unique output filename for this phase

% Reseed the random-number generator for each experiment run
rng('shuffle'); %this is the new way that sets the initial seed using date/time

%% Prepare Psychtoolbox

DEBUG_ME = 0;
if DEBUG_ME == 1
    Screen('Preference','SkipSyncTests', 1); %required for Justin's office iMac until graphics incompatibility comes out
    PsychDebugWindowConfiguration(0,0.5) %set background to semi-transparent to see command window
end

% Get the screen numbers
screens = Screen('Screens');

% Draw to the external screen if avaliable
screenNumber = max(screens);

% Get size of screen
[s_width, s_height]=Screen('WindowSize', screenNumber); %also found in windowRect below

% Get value of color black & white, set other RGB color values for later:
black = BlackIndex(screenNumber);
white = WhiteIndex(screenNumber);
gray = white/2;
lightgray = [220, 220, 220];
green = [0, 255, 0];
red = [255, 0, 0];
blue = [30, 144, 255]; %now Dodger Blue b/c original is too dark [0, 0, 255];
yellow = [255, 255, 0];
%%prepare color for the words
% Open an on screen window with a white background color:
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, black);

% Set blend function for alpha blending
Screen('BlendFunction', window, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

% % We use a normalized color range from now on (can be set with
% PsychDefulatSetup(2). All color values are % specified as numbers between
% 0.0 and 1.0, instead of the usual 0 to % 255 range. This is more
% intuitive: Screen('ColorRange', window, 1, 0);

% Get the center coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Set default text stuff later calls to DrawFormattedText(window, text, 'center', 'center');
Screen('TextFont', window, 'Times'); %default font
Screen('TextSize', window, 44); %default font size
Screen('TextStyle', window, 1); %default font style
Screen('TextColor', window, white); %default font color
Screen('Preference', 'TextAlphaBlending', 0); %default font transparency

flipTime = Screen('GetFlipInterval',window); %for this particular phase (not necessarily the one used in the main TNT phase)
slack = flipTime/2; % start any time-critical flip early enough to allow the flip to take place (use a halfflip); can be used to present at an exact time after a previous stimulus onset [e.g., for 500ms after t_prime, use: "tprime_onset = Screen('Flip', window, tfixation_onset + 0.500 - slack)"]
Hz = 60; %the frame rate of the monitor to be used for the main TNT phase; at 60Hz refresh (standard for LCD), that's 1/60Hz = ~16.67ms per frame; so 116.7ms is 7 frames | 133.3ms is 8 frames use this to establish the jitter time
%Hz=Screen(window,'NominalFrameRate');

% Get the size of the on screen window in pixels
% For help see: Screen WindowSize?
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Get the centre coordinate of the window in pixels
% For help see: help RectCenter
[xCenter, yCenter] = RectCenter(windowRect);

%% Prepare output file

% Open and set-up result file
dataFile = fopen(['results/' baseName '_SleepTrigs.txt'], 'a');

% Print out analysis information
header = sprintf([...
    '*********************************************\n' ...
    '* Experiment: Dreem_Rrr\n' ...
    '* Phase: Nap\n' ...
    '* Script: %s\n' ...
    '* Script Version #: %s\n'...
    '* Date/Time: %s\n' ...
    '* Subject Number: %s\n' ...
    '* DFcond: %d\n' ...
    '* Tcond: %d\n' ...
    '* Version: %s\n' ...
    '* Nap_sounds: %d\t%d (Event Codes: NapSoundA=1; NapSoundB=2, regardless of SoundFile#)\n' ...
    '* Debug: %d\n'...
    '* Screen: %d\n'...
    '* Stims File: %s\n' ...
    '* Results File: %s\n' ...
    '*********************************************\n\n'], ...
    mfilename,VERSION_NO,datestr(now,0),SUBJECT,DFcond,Tcond,Version,SoundFile1,SoundFile2, ...
    DEBUG_ME,screenNumber,'_stims.mat',['results/' baseName '_SleepTrigs.txt']);

fprintf(dataFile,'%s',header);
fprintf('%s',header);

trial_header = sprintf(['RelTriggerTime\tEventCode\tTimestamp\n']);
fprintf(dataFile,trial_header);
fprintf(trial_header);

fclose(dataFile);

%% Prep BioSemi triggers

% Using EEG triggers?
BioSemi = 1; %set to 1 if yes, so that we send triggers

% % %TRIGGER CODES (FOR REFERENCE)
% % Phase start = 8
% % Sound 1 played = 1
% % Sound 2 played = 2
% % N2 manually detected = 3
% % Arousal/transition to non-N2 sleep manually detected = 4
% % Phase end = 9

if BioSemi %zero out all the parallel port pins before beginning
    s = daq.createSession('ni'); %set up the session--initialize session-based interface to NI-DAQ device for triggering
    ch = addDigitalChannel(s,'Dev1','Port1/Line0:7','OutputOnly'); %Set up an 8-bit range as a channel to which events can be written
    outputSingleScan(s,[0 0 0 0 0 0 0 0]) %reset port to zero, see timing requirement above
end

%% Get ready to score sleep!

% Make sure EEG recording has started (if Biosemi)
if BioSemi
    % Alert experimenter to start recording in ActiView
    msg = sprintf('*!*!*!EXPERIMENTER: Make sure EEG recording has started, then press any key*!*!*!\n\n');
    
    DrawFormattedText(window, msg, 'center', 'center', blue);
    Screen('Flip',window);
    WaitSecs(1); %must wait before pressing button
    
    KbWait(); % wait for a button press to move on
    Screen('Flip',window);
    
    %send a trigger code (8) indicating the start of the nap phase
    n_start = GetSecs; %log start time for output file (all trigger times in text output will be relative to this)
    trig_time = n_start; %relative trigger time (same as above for this first instance only)
    trig_code = fliplr((dec2bin(8,8))) - '0'; %turn the first input to (flipped) 8-bit binary vector (the string to vector conversion happens with -'0')
    outputSingleScan(s,trig_code)
    WaitSecs(0.004) %pulse on for 4 milliseconds; must be >than time resolution of hardware [try (1000/<EEG sampling rate>)+2ms]
    outputSingleScan(s,[0 0 0 0 0 0 0 0]) %reset port to zero, see timing requirement above
    
    %log output
    event_info = sprintf('%.3f\t8\t%s\n',trig_time,datestr(now,'HH:MM:SS.FFF')); %Note this line is different based on the trigger type
    dataFile = fopen(['results/' baseName '_SleepTrigs.txt'], 'a');
    fprintf(dataFile,event_info);
    fprintf(event_info);
    fclose(dataFile);
    
    WaitSecs(3); %wait
end

%establish sounds
sound1 = ['./stimuli/Sound' num2str(SoundFile1) '.wav']; %SoundA
sound2 = ['./stimuli/Sound' num2str(SoundFile2) '.wav']; %SoundB
Slist=[1,2]; %how many sounds will be played
jitter=[10,11,12,13,14,15,16,17,18,19,20]; %possible jitter values (in seconds) for  ISI (between 10-20s); additional jitter between 0-1 seconds included below

% Perform basic initialization of the sound driver:
InitializePsychSound;

%% Here we go!!!

% Lets write three lines of text to the screen, the first and second right
% after one another, and the third with a line space in between. To add
% line spaces we use the special characters "\n"
line1 = 'when get into N2 stage';
line2 = '\n press return';
line3 = '\n\n to start the countdown timer';

% Draw all the text in one go
Screen('TextSize', window, 60);
DrawFormattedText(window, [line1 line2 line3],...
    'center', screenYpixels * 0.25, white);

% Flip to the screen
Screen('Flip', window)

% Wait for the experimenter to spot signs of N2 sleep, which will then
% start a 60-second countdown timer
done = 0;
while done == 0
    [down, kbsecs, KeyCode] = KbCheck;
    if KeyCode(return_key) == 1 %keycode 40 = "return" on mac. Use KbDemo to figure out other keycodes in PTB
        done = 1;
        if BioSemi
            trig_time = GetSecs - n_start; %relative trigger time
            trig_code = fliplr((dec2bin(3,8))) - '0'; %turn the first input to (flipped) 8-bit binary vector (the string to vector conversion happens with -'0')
            outputSingleScan(s,trig_code)
            WaitSecs(0.004) %pulse on for 4 milliseconds; must be >than time resolution of hardware [try (1000/<EEG sampling rate>)+2ms]
            outputSingleScan(s,[0 0 0 0 0 0 0 0]) %reset port to zero, see timing requirement above
            
            %log output
            event_info = sprintf('%.3f\t3\t%s\n',trig_time,datestr(now,'HH:MM:SS.FFF')); %note this has the trigger code hard coded
            dataFile = fopen(['results/' baseName '_SleepTrigs.txt'], 'a');
            fprintf(dataFile,event_info);
            fprintf(event_info);
            fclose(dataFile);
        end
    end
end

%start countdown
run Timer.m %start 60-second countdown, which can be reset for arousals/transitions to other sleep stages

%Once the timer has reached 0 (without arousals/transitions to other
%stages), begin playback of the two sounds, each presented 15 times in
%block randomized order
for tr = 1:15
    DrawFormattedText(window, 'sounds on', 'center', 'center',red);
    Screen('Flip', window)
    x=Shuffle(Slist); %figure out which sound to present first in a pair
    t=Shuffle(jitter); %figure out which random jitter values to use for each sound in a pair
    ss=t(1,1)+rand; %first jitter value including extra jitter between 0-1s
    sss=t(1,2)+rand; %second jitter value including extra jitter between 0-1s
    
    %get the appropriate first sound in a pair ready
    if x(1,1)==1
        wavfilename=sound1;
        sound_num = 1;
    elseif x(1,1)==2
        wavfilename=sound2;
        sound_num = 2;
    end
    [y, freq] = psychwavread(wavfilename); % Read WAV file from filesystem:
    wavedata = y';
    nrchannels = size(wavedata,1);
    if nrchannels < 2
        wavedata = [wavedata ;
            wavedata];
        nrchannels = 2;
    end
    
    try
        % Try with the 'freq'uency we wanted:
        pahandle = PsychPortAudio('Open', [], [], 0, freq, nrchannels);
    catch
        % Failed. Retry with default frequency as suggested by device:
        fprintf('\nCould not open device at wanted playback frequency of %i Hz. Will retry with device default frequency.\n', freq);
        fprintf('Sound may sound a bit out of tune, ...\n\n');
        
        psychlasterror('reset');
        pahandle = PsychPortAudio('Open', [], [], 0, [], nrchannels);
    end
    
    % Fill the audio playback buffer with the audio data 'wavedata':
    PsychPortAudio('FillBuffer', pahandle, wavedata);
    
    % Play the sound
    t1 = PsychPortAudio('Start', pahandle, 1, 0, 1);
    if BioSemi
        trig_time = GetSecs - n_start; %relative trigger time
        trig_code = fliplr((dec2bin(sound_num,8))) - '0'; %turn the first input to (flipped) 8-bit binary vector (the string to vector conversion happens with -'0')
        outputSingleScan(s,trig_code)
        WaitSecs(0.004) %pulse on for 4 milliseconds; must be >than time resolution of hardware [try (1000/<EEG sampling rate>)+2ms]
        outputSingleScan(s,[0 0 0 0 0 0 0 0]) %reset port to zero, see timing requirement above
        
        %log output
        event_info = sprintf('%.3f\t%d\t%s\n',trig_time,sound_num,datestr(now,'HH:MM:SS.FFF'));
        dataFile = fopen(['results/' baseName '_SleepTrigs.txt'], 'a');
        fprintf(dataFile,event_info);
        fprintf(event_info);
        fclose(dataFile);
    end
    
    clear ans
    
    %Jittered ISI, poll for possible arousals/sleep transitions
    getkeywait(ss) %wait the jitter duration, while still polling for possible arousals/transitions to other stage, which will restart timer
    if ans == 32 %possible arousal/transition--hold up!
        
        % Arousal/transition to another stage detected!
        DrawFormattedText(window, 'sound off', 'center', 'center', red);
        Screen('Flip', window);
        if Biosemi
            trig_time = GetSecs - n_start; %relative trigger time
            trig_code = fliplr((dec2bin(4,8))) - '0'; %turn the first input to (flipped) 8-bit binary vector (the string to vector conversion happens with -'0')
            outputSingleScan(s,trig_code)
            WaitSecs(0.004) %pulse on for 4 milliseconds; must be >than time resolution of hardware [try (1000/<EEG sampling rate>)+2ms]
            outputSingleScan(s,[0 0 0 0 0 0 0 0]) %reset port to zero, see timing requirement above
            
            %log output
            event_info = sprintf('%.3f\t4\t%s\n',trig_time,datestr(now,'HH:MM:SS.FFF')); %note this has the trigger code hard coded
            dataFile = fopen(['results/' baseName '_SleepTrigs.txt'], 'a');
            fprintf(dataFile,event_info);
            fprintf(event_info);
            fclose(dataFile);
        end
        pause
        
        % Wait for experimenter to see signs of N2 sleep again, at which
        % point the 60-second timer will be restarted
        done = 0;
        while done == 0
            [down, kbsecs, KeyCode] = KbCheck;
            if KeyCode(return_key) == 1 %keycode 40 = "return" on mac. Use KbDemo to figure out other keycodes in PTB
                if BioSemi
                    trig_time = GetSecs - n_start; %relative trigger time
                    trig_code = fliplr((dec2bin(3,8))) - '0'; %turn the first input to (flipped) 8-bit binary vector (the string to vector conversion happens with -'0')
                    outputSingleScan(s,trig_code)
                    WaitSecs(0.004) %pulse on for 4 milliseconds; must be >than time resolution of hardware [try (1000/<EEG sampling rate>)+2ms]
                    outputSingleScan(s,[0 0 0 0 0 0 0 0]) %reset port to zero, see timing requirement above
                    
                    %log output
                    event_info = sprintf('%.3f\t3\t%s\n',trig_time,datestr(now,'HH:MM:SS.FFF')); %note this has the trigger code hard coded
                    dataFile = fopen(['results/' baseName '_SleepTrigs.txt'], 'a');
                    fprintf(dataFile,event_info);
                    fprintf(event_info);
                    fclose(dataFile);
                end
                done = 1;
            end
        end
        
        run timer.m %start 60-second countdown, which can be reset for arousals/transitions to other sleep stages, which will allow us to resume sound presentations from where we left off
        
    end
    
    DrawFormattedText(window, 'sound on', 'center', 'center', red);
    Screen('Flip', window);
    
    % Present the second sound in a pair, so long as there is no arousal
    if x(1,1)==1
        wavfilename=sound2;
        sound_num = 2;
    elseif x(1,1)==2
        wavfilename=sound1;
        sound_num = 1;
    end
    if nrchannels < 2
        wavedata = [wavedata ;
            wavedata];
        nrchannels = 2;
    end
    [y, freq] = psychwavread(wavfilename); % Read WAV file from filesystem:
    wavedata = y';
    nrchannels = size(wavedata,1);
    try
        % Try with the 'freq'uency we wanted:
        pahandle = PsychPortAudio('Open', [], [], 0, freq, nrchannels);
    catch
        % Failed. Retry with default frequency as suggested by device:
        fprintf('\nCould not open device at wanted playback frequency of %i Hz. Will retry with device default frequency.\n', freq);
        fprintf('Sound may sound a bit out of tune, ...\n\n');
        
        psychlasterror('reset');
        pahandle = PsychPortAudio('Open', [], [], 0, [], nrchannels);
    end
    
    % Fill the audio playback buffer with the audio data 'wavedata':
    PsychPortAudio('FillBuffer', pahandle, wavedata);
    
    % Play the sound
    t1 = PsychPortAudio('Start', pahandle, 1, 0, 1);
    if BioSemi
        trig_time = GetSecs - n_start; %relative trigger time
        trig_code = fliplr((dec2bin(sound_num,8))) - '0'; %turn the first input to (flipped) 8-bit binary vector (the string to vector conversion happens with -'0')
        outputSingleScan(s,trig_code)
        WaitSecs(0.004) %pulse on for 4 milliseconds; must be >than time resolution of hardware [try (1000/<EEG sampling rate>)+2ms]
        outputSingleScan(s,[0 0 0 0 0 0 0 0]) %reset port to zero, see timing requirement above
        
        %log output
        event_info = sprintf('%.3f\t%d\t%s\n',trig_time,sound_num,datestr(now,'HH:MM:SS.FFF'));
        dataFile = fopen(['results/' baseName '_SleepTrigs.txt'], 'a');
        fprintf(dataFile,event_info);
        fprintf(event_info);
        fclose(dataFile);
    end
    
    clear ans
    
    getkeywait(sss) %wait the second jitter duration, while still polling for possible arousals/transitions to other stage, which will restart timer
    if ans == 32 %possible arousal/transition--hold up!
        
        DrawFormattedText(window, 'sound off', 'center', 'center', red);
        Screen('Flip', window);
        if BioSemi
            trig_time = GetSecs - n_start; %relative trigger time
            trig_code = fliplr((dec2bin(4,8))) - '0'; %turn the first input to (flipped) 8-bit binary vector (the string to vector conversion happens with -'0')
            outputSingleScan(s,trig_code)
            WaitSecs(0.004) %pulse on for 4 milliseconds; must be >than time resolution of hardware [try (1000/<EEG sampling rate>)+2ms]
            outputSingleScan(s,[0 0 0 0 0 0 0 0]) %reset port to zero, see timing requirement above
            
            %log output
            event_info = sprintf('%.3f\t4\t%s\n',trig_time,datestr(now,'HH:MM:SS.FFF')); %note this has the trigger code hard coded
            dataFile = fopen(['results/' baseName '_SleepTrigs.txt'], 'a');
            fprintf(dataFile,event_info);
            fprintf(event_info);
            fclose(dataFile);
        end
        pause
        
        done = 0;
        while done == 0
            [down, kbsecs, KeyCode] = KbCheck;
            if KeyCode(return_key) == 1 %keycode 40 = "return" on mac. Use KbDemo to figure out other keycodes in PTB
                if BioSemi
                    trig_time = GetSecs - n_start; %relative trigger time
                    trig_code = fliplr((dec2bin(3,8))) - '0'; %turn the first input to (flipped) 8-bit binary vector (the string to vector conversion happens with -'0')
                    outputSingleScan(s,trig_code)
                    WaitSecs(0.004) %pulse on for 4 milliseconds; must be >than time resolution of hardware [try (1000/<EEG sampling rate>)+2ms]
                    outputSingleScan(s,[0 0 0 0 0 0 0 0]) %reset port to zero, see timing requirement above
                    
                    %log output
                    event_info = sprintf('%.3f\t3\t%s\n',trig_time,datestr(now,'HH:MM:SS.FFF')); %note this has the trigger code hard coded
                    dataFile = fopen(['results/' baseName '_SleepTrigs.txt'], 'a');
                    fprintf(dataFile,event_info);
                    fprintf(event_info);
                    fclose(dataFile);
                end
                done = 1;
            end
        end
        run timer.m
    end
end

if BioSemi %log end of nap phase of the experiment w/ triger pulse
    trig_time = GetSecs - n_start; %relative trigger time
    trig_code = fliplr((dec2bin(9,8))) - '0'; %turn the first input to (flipped) 8-bit binary vector (the string to vector conversion happens with -'0')
    outputSingleScan(s,trig_code)
    WaitSecs(0.004) %pulse on for 4 milliseconds; must be >than time resolution of hardware [try (1000/<EEG sampling rate>)+2ms]
    outputSingleScan(s,[0 0 0 0 0 0 0 0]) %reset port to zero, see timing requirement above
    
    %log output
    event_info = sprintf('%.3f\t9\t%s\n',trig_time,datestr(now,'HH:MM:SS.FFF')); %note this has the trigger code hard coded
    dataFile = fopen(['results/' baseName '_SleepTrigs.txt'], 'a');
    fprintf(dataFile,event_info);
    fprintf(event_info);
    fclose(dataFile);
end

%% Clean up

msg = sprintf('phase completed!\n');
DrawFormattedText(window, msg, 'center', 'center', gray);
Screen('Flip',window);
WaitSecs(2);

% Clear the screen
sca;

% Done. Close screen and finish:
ShowCursor;
Screen('CloseAll');
clc; %clear command window
fclose('all');
Priority(0);
