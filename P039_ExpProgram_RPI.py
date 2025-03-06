#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Tues Nov 19 2024
@author: cyruskirkman, Zayaan K., & Arnav R.

Last updated: 2025-03-05

    
P039 - Selective Aversion to Predator Eye Orientation in Pigeons

This is the main code for Cyrus Kirkman, Zayaan Khan, and Arnav Ranade's P039a 
project studying eye orientation (distance between eyes) and its impact on pigeon
response rates overall. In regards to probe stimuli, we created a stimulus set
in which the eyes were gradually moved outwards from one probe stimuli to the 
next. Prior to either the autoshaping or the preferential choice task phase, we 
provided a "pre-training" phase to the birds to allow birds that had not been 
actively participating in other trials a chance to grow reaccustomed to the
procedure and apparatus.
    
    1) Mixed instrumental/autoshaping: Each trial began with a black screen for 
    10s, after which a single neutral stimulus would appear in the middle of the screen. 
	The first experiment utilized a mixed autoshaping/instrumental procedure. 
    Each trial began with a black screen for 10 s, after which a single neutral 
    stimulus would appear in the middle of the screen. Food reinforcement was 
    provided after the 30s interval concluded or immediately following approximately 
    five pecks (RR5) at the presented stimulus; pigeons could only receive a single 
    reward per trial. A variable ITI (between 10 - 20 s) separated trials to avoid 
    prediction effects. For the first five trials of each session, birds were presented 
    with one training stimulus from each training set, which was pseudo-randomly 
    selected without replacement from the 25 possible training stimuli. On the 
    sixth trial, subjects were shown either P1 or P5 (see Table 2 for counterbalancing 
    order), which were the probe stimuli at either end of the prey/predator eye 
    orientation spectrum. Probe trials were otherwise identical to neutral 
    stimuli trials in schedule and timing of reinforcement. Trials 7 - 11 each 
    contained another unique training stimulus from each set and trial 12 contained 
    the opposite probe stimulus (P5 or P1). The early order of probe stimuli trials 
    was explicitly counterbalanced across subjects to account for any order, 
    repetition, or novelty/habituation effects. If the eye probe stimuli elicit 
    fear unconditionally, we might expect to see more fear-like responses in early 
    trials. Throughout the remainder of the session, 2 - 8 pseudo-randomly selected 
    training stimuli trials separated probe trials to prevent learned prediction effects. 
    The remaining three probe trial types (P2, P3, and P4) were cycled through 
    in a preset order (Table 2), then the order of all five probe stimuli were 
    quasi-random sampled without replacement for the remainder of the session, 
    which inherently rendered more than two consecutive probe repetitions impossible. 
    Training stimuli were always selected via quasi-random sampling without replacement 
    from the sample set of 25; no more than two of stimuli of the same training 
    set were shown consecutively.


        
    2) Preferential Choice Task: The next phase consisted of a choice task, 
    where two different eye stimuli from the set were presented to the birds, and
    (10) pecks at either one would allow us to gauge preference between eye stimuli
    with varying distance between pupils. The same exact five probe stimuli in phase
    1 were utilized in this phase 2 choice task. Pigeons were required to peck at
    one of the two stimuli roughly 10 times in order to receive a food reward and 
    move on to the next set of two stimuli. For displaying stimuli, the trial order
    was regulated on a quasi-random basis; the same stimulus was never presented 
    on more than three consecutive trials. Phase 2 sessions concluded after 80 trials
    were completed or 90 minutes elapsed, whichever came first.
"""

# Prior to running any code, its conventional to first import relevant 
# libraries for the entire script. These can range from python libraries (sys)
# or sublibraries (setrecursionlimit) that are downloaded to every computer
# along with python, or other files within this folder (like control_panel or 
# maestro).
# =============================================================================
from copy import deepcopy
from csv import writer, QUOTE_MINIMAL, DictReader
from datetime import datetime, timedelta, date
from sys import setrecursionlimit, path as sys_path
from tkinter import Toplevel, Canvas, BOTH, TclError, Tk, Label, Button, \
     StringVar, OptionMenu, IntVar, Radiobutton
from time import time, sleep, strftime
from os import getcwd, popen, mkdir, path as os_path
from PIL import ImageTk, Image  
from random import choice, shuffle
from subprocess import run

# The first variable declared is whether the program is the operant box version
# for pigeons, or the test version for humans to view. The variable below is 
# a T/F boolean that will be referenced many times throughout the program 
# when the two options differ (for example, when the Hopper is accessed or
# for onscreen text, etc.). It is changed automatically based on whether
# the program is running in operant boxes (True) or not (False). It is
# automatically set to True if the user is "blaisdelllab" (e.g., running
# on a rapberry pi) or False if not. The output of os_path.expanduser('~')
# should be "/home/blaisdelllab" on the RPis

if os_path.expanduser('~').split("/")[2] =="blaisdelllab":
    operant_box_version = True
    print("*** Running operant box version *** \n")
else:
    operant_box_version = False
    print("*** Running test version (no hardware) *** \n")

# Import hopper/other specific libraries from files on operant box computers
try:
    if operant_box_version:
        # Import additional libraries...
        import pigpio # import pi, OUTPUT
        import csv
        
        # Setup GPIO numbers (NOT PINS; gpio only compatible with GPIO num)
        servo_GPIO_num = 2
        hopper_light_GPIO_num = 13
        house_light_GPIO_num = 21
        string_LED_GPIO_num = 5 # Only in box 1
        
        # Setup use of pi()
        rpi_board = pigpio.pi()
        
        # Then set each pin to output 
        rpi_board.set_mode(servo_GPIO_num,
                           pigpio.OUTPUT) # Servo motor...
        rpi_board.set_mode(hopper_light_GPIO_num,
                           pigpio.OUTPUT) # Hopper light LED...
        rpi_board.set_mode(house_light_GPIO_num,
                           pigpio.OUTPUT) # House light LED...
        rpi_board.set_mode(string_LED_GPIO_num,
                           pigpio.OUTPUT) # House light LED...
        
        # Setup the servo motor 
        rpi_board.set_PWM_frequency(servo_GPIO_num,
                                    50) # Default frequency is 50 MhZ
        
        # Next grab the up/down 
        hopper_vals_csv_path = str(os_path.expanduser('~')+"/Desktop/Box_Info/Hopper_vals.csv")
        
        # Store the proper UP/DOWN values for the hopper from csv file
        up_down_table = list(csv.reader(open(hopper_vals_csv_path)))
        hopper_up_val = up_down_table[1][0]
        hopper_down_val = up_down_table[1][1]
        
        # Lastly, run the shell script that maps the touchscreen to operant box monitor
        popen("sh /home/blaisdelllab/Desktop/Hardware_Code/map_touchscreen.sh")
                             
        
except ModuleNotFoundError:
    input("ERROR: Cannot find hopper hardware! Check desktop.")

# Below  is just a safety measure to prevent too many recursive loops). It
# doesn't need to be changed.
setrecursionlimit(5000)

"""
The code below jumpstarts the loop by first building the hopper object and 
making sure everything is turned off, then passes that object to the
control_panel. The program is largely recursive and self-contained within each
object, and a macro-level overview is:
    
    ControlPanel -----------> MainScreen ------------> PaintProgram
         |                        |                         |
    Collects main           Runs the actual         Gets passed subject
    variables, passes      experiment, saves        name, but operates
    to Mainscreen          data when exited          independently
    

"""

# The first of three objects we declare is the ExperimentalControlPanel (CP). It
# exists "behind the scenes" throughout the entire session, and if it is exited,
# the session will terminate.
class ExperimenterControlPanel(object):
    # The init function declares the inherent variables within that object
    # (meaning that they don't require any input).
    def __init__(self):
        # Next up, we need to do a couple things that will be different based
        # on whether the program is being run in the operant boxes or on a 
        # personal computer. These include setting up the hopper object so it 
        # can be referenced in the future, or the location where data files
        # should be stored.
        if operant_box_version:
            # Setup the data directory in "Documents"
            self.data_folder = "P039_data" # The folder within Documents where subject data is kept
            self.data_folder_directory = str(os_path.expanduser('~'))+"/Desktop/Data/" + self.data_folder
        else: # If not, just save in the current directory the program us being run in 
            self.data_folder_directory = getcwd() + "/data"
            if not os_path.isdir(self.data_folder_directory):
                mkdir(self.data_folder_directory)
                print("\n ** NEW DATA FOLDER CREATED **")
            
        
        # setup the root Tkinter window
        self.control_window = Tk()
        self.control_window.title("P039 Control Panel")
        ##  Next, setup variables within the control panel
        # Subject ID
        self.pigeon_name_list = ["Peach","Wario", "Jagger", "Herriot"]
        self.pigeon_name_list.sort() # This alphabetizes the list
        self.pigeon_name_list.insert(0, "TEST")
        
        Label(self.control_window,
              text="Pigeon Name:").pack()
        self.subject_ID_variable = StringVar(self.control_window)
        self.subject_ID_variable.set("Select")
        self.subject_ID_menu = OptionMenu(self.control_window,
                                          self.subject_ID_variable,
                                          *self.pigeon_name_list,
                                          command = self.set_pigeon_ID).pack()
        
        
        # Training phases
        Label(self.control_window,
              text = "Select phase:").pack()
        self.training_phase_variable = IntVar()
        self.training_phase_name_list = ["1: Pre-training",
                                         "2: Autoshaping/Instrumental",
                                         "3: Choice Task"]
        for t_name in self.training_phase_name_list:
            Radiobutton(self.control_window,
                        variable = self.training_phase_variable,
                        text = t_name,
                        value = self.training_phase_name_list.index(t_name)).pack()
        self.training_phase_variable.set(0) # Default set to first training phase
        
        # Record video variable?
        Label(self.control_window,
              text = "Record and save video?").pack()
        self.record_video_variable = IntVar()
        Radiobutton(self.control_window,
                    variable = self.record_video_variable,
                    text = "Yes",
                    value = True).pack()
        Radiobutton(self.control_window,
                    variable = self.record_video_variable,
                    text = "No",
                    value = False).pack()
        self.record_video_variable.set(True) # Default set to True
        
        
        # Record data variable?
        Label(self.control_window,
              text = "Record data in seperate data sheet?").pack()
        self.record_data_variable = IntVar()
        Radiobutton(self.control_window,
                    variable = self.record_data_variable,
                    text = "Yes",
                    value = True).pack()
        Radiobutton(self.control_window,
                    variable = self.record_data_variable,
                    text = "No",
                    value = False).pack()
        self.record_data_variable.set(True) # Default set to True
        
        
        # Start button
        self.start_button = Button(self.control_window,
                                   text = 'Start program',
                                   bg = "green2",
                                   command = self.build_chamber_screen).pack()
        # Stop button 
        self.stop_button = Button(self.control_window,
                                   text = 'Stop program',
                                   bg = "red",
                                   command = self.stop_program
                                   ).pack()
        
        # This makes sure that the control panel remains onscreen until exited
        self.control_window.mainloop() # This loops around the CP object
        
        
    def set_pigeon_ID(self, pigeon_name):
        # This function checks to see if a pigeon's data folder currently 
        # exists in the respective "data" folder within the macro Data
        # folder and, if not, creates one.
        try:
            if not os_path.isdir(self.data_folder_directory + pigeon_name):
                mkdir(os_path.join(self.data_folder_directory, pigeon_name))
                print("\n ** NEW DATA FOLDER FOR %s CREATED **" % pigeon_name.upper())
        except FileExistsError:
            print(f"DATA FOLDER FOR {pigeon_name.upper()} EXISTS")
        except FileNotFoundError:
            print("ERROR: Cannot find data folder!")
    
    def stop_program(self):
        # This is the function that is called whenever the red "Stop program"
        # button is pressed. It will close any Mainscreen object and clean the 
        # GPIO board (including turning off the lights and returning the hopper
        # to the down state, if up)
        print("Stop program button pressed.")
                
                
    def build_chamber_screen(self):
        # Once the green "start program" button is pressed, then the mainscreen
        # object is created and pops up in a new window. It gets passed the
        # important inputs from the control panel.
        # print(str(self.stimulus_set_variable.get())[0])
        if self.subject_ID_variable.get() in self.pigeon_name_list:
            print("Start Program Button Pressed") 
            self.MS = MainScreen(
                str(self.subject_ID_variable.get()), # subject_ID
                self.record_data_variable.get(), # Boolean for recording data (or not)
                self.data_folder_directory, # directory for data folder
                self.training_phase_variable.get(), # Which training phase
                self.training_phase_name_list, # list of training phases
                self.record_video_variable.get() # Record video
                )
        else:
            print("\n ERROR: Input Correct Pigeon ID Before Starting Session")
            


# Then, setup the MainScreen object
class MainScreen(object):
    # First, we need to declare several functions that are 
    # called within the initial __init__() function that is 
    # run when the object is first built:
    
    def __init__(self, subject_ID, record_data, data_folder_directory,
                 training_phase, training_phase_name_list, 
                 record_video):
        ## Firstly, we need to set up all the variables passed from within
        # the control panel object to this MainScreen object. We do this 
        # by setting each argument as "self." objects to make them global
        # within this object.
        
        # Setup variables passed from Control Panel
        self.subject_ID = subject_ID # Subject Name
        self.record_data = record_data # T/F record data
        self.data_folder_directory = data_folder_directory
        self.training_phase = training_phase # the phase of training as a number (0-2)
        self.training_phase_name_list = training_phase_name_list 
        self.record_video = record_video # T/F
        
        # In order to properly counter-balance the early order of probe
        # stimuli, we need to assign subjects to one of four groups. Each group 
        # will recive the stimuli in a different order:
        
        # For our initial portion of the autoshaping/mixed instrumental portion,
        # we assigned subjects to one of four different groups. G1, G2, G3, or G4
        # G1 would recieve probe stimuli in the following order: P1-P5-P2-P3-P4
        # G2 would recieve probe stimuli in the following order: P1-P5-P4-P3-P2
        # G3 would recieve probe stimuli in the following order: P5-P1-P4-P3-P2
        # G4 would recieve probe stimuli in the following order: P5-P1-P4-P3-P2
        
        # This counterbalancing schedule was maintained across multiple sessions.
        dict_of_subject_assignments = {
            "TEST": 1,
            "Peach": 1,
            "Wario": 2,
            "Jagger": 3,
            "Herriot": 4
            }
        
        self.control_condition = dict_of_subject_assignments[self.subject_ID]
        
        if self.control_condition       == 1:
            self.probe_stimulus_order   = [1, 5, 2, 3, 4]
        elif self.control_condition     == 2:
            self.probe_stimulus_order   = [1, 5, 4, 3, 2]
        elif self.control_condition     == 3:
            self.probe_stimulus_order   = [5, 1, 2, 3, 4]
        elif self.control_condition     == 4:
            self.probe_stimulus_order   = [5, 1, 4, 3, 2]
            
        ## Define some other variables that will be important for the procedure
        self.autoshaping_RR = 5
        self.choice_task_RR = 10
        self.trial_num = 0 # counter for current trial in session
        self.trial_stage = 0 # Trial substage (we have 2: blank screen/stimulus presentation or choice trial/terminal link)
        self.max_number_of_reinforced_trials = 90 # Max number of trials within a session (three trials per stimulus)
        self.trial_type = "NA" # Does not change if pretraining
        
        # Video recording variables
        self.currently_recording = False  # Describes if the cameras are currently recording (never for first ITI)
        self.top_filename  = "NA"
        self.side_filename = "NA"
        
        # Timing variables
        self.auto_reinforcer_timer = 30 * 1000 # Time (ms) before reinforcement for AS
        self.start_time = None # This will be reset once the session actually starts
        self.trial_start = None # Duration into each trial as a second count, resets each trial
        self.session_duration = datetime.now() + timedelta(minutes = 90) # Max session time is 90 min
        if self.training_phase in [0, 1]:
            self.ITI_duration = 10 * 1000 # duration of inter-trial interval (ms) is variable between 10 - 20 s
        elif self.training_phase == 2:
            self.ITI_duration = 20 * 1000 # duration of inter-trial interval (ms)
        self.hopper_duration = 5 * 1000 # duration of accessible hopper (ms)
        self.trial_delay_duration = 10 * 1000 # delay after a trial starts but before the stimulus is presented (screen is black)
        
        # These are additional stimuli-specific variables...
        self.image_center = [512,384]
        if self.training_phase == 2:
            self.choice_key_coord_dict = {
                "left_choice"  : [211.5, 374],
                "right_choice" : [812.5, 374]
                } 
        self.neutral_feedback_color = "#2596BE" # For the blue circle in pre-training
        self.background_color = "#7F7F7F" # Background color for trials for all stimuli
        self.yellow_color = "#E8D24C"
        self.brown_color = "#31131E"
        
        ## Setup data structure...
        self.session_data_frame = [] #This where trial-by-trial data is stored
        header_list = ["Subject", "Date", "ExpPhaseNum", "ExpPhaseName", 
                       "SessionTime", "TrialNum", "TrialType", "EventType",
                       "TrialSubStage", "TrialTime", "TrialSubStageTimer",
                       "ITIDuration", "Xcord","Ycord", "CenterPythDist", 
                       "LeftPythDist", "RightPythDist", "CenterStim",
                       "LeftStim", "LeftStimTrainingSet", "LeftStimNumber",
                       "RightStim", "RightStimTrainingSet", "RightStimNumber",
                       "SubPhase1RR", "SubPhase1LeftButtonPresses",
                       "SubPhase1RightButtonPresses", "SubPhase2RR",
                       "SubPhase2ButtonPresses", "VideoRecorded",
                       "TopVideoFileName", "SideVideoFileName"] # Column headers
        self.session_data_frame.append(header_list) # First row of matrix is the column headers
        self.myFile_loc = 'FILL' # To be filled later on after Pig. ID is provided (in set vars func below)

        ## Set up the visual Canvas
        self.root = Toplevel()
        self.root.title(f"P039: {self.training_phase_name_list[self.training_phase][3:]}") # this is the title of the windows
        self.mainscreen_height = 768 # height of the experimental canvas screen
        self.mainscreen_width = 1024 # width of the experimental canvas screen
        self.root.bind("<Escape>", self.exit_program) # bind exit program to the "esc" key
        
        # If the version is the one running in the boxes, run some independent processes
        if operant_box_version:
            # Keybind relevant keys
            self.cursor_visible = True # Cursor starts on...
            self.change_cursor_state() # turn off cursor UNCOMMENT
            self.root.bind("<c>",
                           lambda event: self.change_cursor_state()) # bind cursor on/off state to "c" key
            # Then fullscreen (on a 1024x768p screen). Assumes that both screens
            # that are being used have identical dimensions
            self.root.geometry(f"{self.mainscreen_width}x{self.mainscreen_height}+1920+0")
            self.root.attributes('-fullscreen',
                                 True)
            self.mastercanvas = Canvas(self.root,
                                   bg="black")
            self.mastercanvas.pack(fill = BOTH,
                                   expand = True)
        # If we want to run a "human-friendly" version
        else: 
            # No keybinds and  1024x768p fixed window
            self.mastercanvas = Canvas(self.root,
                                   bg="black",
                                   height=self.mainscreen_height,
                                   width = self.mainscreen_width)
            self.mastercanvas.pack()
        
        ## Finally, start the recursive loop that runs the program:
        self.place_birds_in_box()

    def place_birds_in_box(self):
        # This is the default screen run until the birds are placed into the
        # box and the space bar is pressed. It then proceedes to the ITI. It only
        # runs in the operant box version. After the space bar is pressed, the
        # "first_ITI" function is called for the only time prior to the first trial
        
        def first_ITI(event):
            # Is initial delay before first trial starts. It first deletes all the
            # objects off the mnainscreen (making it blank), unbinds the spacebar to 
            # the first_ITI link, followed by a s pause before the first trial to 
            # let birds settle in and acclimate.
            print("Spacebar pressed -- SESSION STARTED") 
            self.mastercanvas.delete("all")
            self.root.unbind("<space>")
            self.start_time = datetime.now() # Set start time
            
            if operant_box_version:
                rpi_board.write(string_LED_GPIO_num,
                    True) # Turn on the LED strings
            
            # First set up the path to the stimulus identity .csv document
            stimuli_csv_path = "P039a_Stimuli/P039a_stimuli_assignments.csv"
                
            # Import the used sample stimuli, their respective training set
            # numbers (class) and stimulus numbers.
            with open(stimuli_csv_path, 'r', encoding='utf-8-sig') as f:
                dict_reader = DictReader(f) 
                self.tenative_stimuli_identity_d_list = list(dict_reader)
                                                                
            # Once the list of dictionaries is written, we can use it to assign
            # the stimuli to each trial of the session. We do this by writing
            # each of the stimuli to a list.
            self.trial_stimulus_order = []
            
            # For the first five trials of each session, birds were presented
            # with one training stimulus from each training set, which was
            # pseudo-randomly selected without replacement from the 25 possible
            # training stimuli.
            if self.training_phase == 1:
                # First 30 trials are set as 5 control, 1 probe, 5 control, etc.
                while len(self.trial_stimulus_order) < 30:
                    # First, select the first five stimuli
                    five_classes = list(range(1, 6))
                    shuffle(five_classes)
                    # Next, selecting actual stimuli from classes
                    for class_num in five_classes:
                        options = [] # Possible stimuli
                        for d in self.tenative_stimuli_identity_d_list: # Cycle through all stimuli...
                            if d['TrainingSet'] == str(class_num): # ...until we find the matching class number
                                if d not in self.trial_stimulus_order: # No repeats
                                    options.append(d)

                        # Chose stimuli from options
                        chosen_stim = choice(options)
                        self.trial_stimulus_order.append(chosen_stim)
                            
                    # Then, we select the relevant probe stimuli
                    probe_trial_num = int((len(self.trial_stimulus_order) / 5) - 1) # Assumes 5 stimuli in between probes
                    probe_stim_number = self.probe_stimulus_order[probe_trial_num]
                    for d in self.tenative_stimuli_identity_d_list: # Cycle through all stimuli...
                        if d['TrainingSet'] == "0": # Probe stimuli
                            if d['StimulusNum'] == str(probe_stim_number):
                                self.trial_stimulus_order.append(d)
                # Add 60 more
                for iteration in [0,1]: # Run twice
                    while True:
                        bad_shuffle = False
                        shuffle(self.tenative_stimuli_identity_d_list)
                        for i in list(range(2, 30)): # Assumes len(self.tenative_stimuli_identity_d_list) == 30
                            d1 = self.tenative_stimuli_identity_d_list[i]
                            c1 = d1["TrainingSet"]
                            d2 = self.tenative_stimuli_identity_d_list[i - 1]
                            c2 = d2["TrainingSet"]
                            d3 = self.tenative_stimuli_identity_d_list[i - 2]
                            c3 = d3["TrainingSet"]
                            if c1 == c2 == c3:
                                bad_shuffle = True
                        # Break if good shuffle
                        if bad_shuffle == False:
                            break
                            
                    # Once a good shuffle is established
                    for d in self.tenative_stimuli_identity_d_list:
                        self.trial_stimulus_order.append(d)
                
                # Finally, load the image files into the dictionary:
                for i in self.trial_stimulus_order:
                    i["img"] = ImageTk.PhotoImage(Image.open(f'P039a_Stimuli/{i["Name"]}'))
                    if int(i["TrainingSet"]) == 0:
                        i["trial_type"] = "probe"
                    else:
                        i["trial_type"] = "control"
            
            # For the binary choice task
            elif self.training_phase == 2:
                # Compared one class of control stimuli to 
                comparison_control_stimuli_class = 5
                # Remove all non-relevant stimuli; utilize 10 total
                self.utilized_trials = []
                for d in self.tenative_stimuli_identity_d_list:
                    if int(d["TrainingSet"]) in [0, comparison_control_stimuli_class]:
                        self.utilized_trials.append(d)
                        
                # Once we collect our 10 choice types, then we need to create
                # permuatations of each combination for trials. These will
                # be every possible combination of Probe v. Probe, Probe v. 
                # Control, and Control v. Control for a total of 45 trials.
                # Furthermore, trials had to flip left/right orientation for 
                # each combination for a total of 90 unique trials.
                
                permutations = []
                for i in range(len(self.utilized_trials)):
                    for j in range(len(self.utilized_trials)):
                        if i != j:
                            permutations.append((self.utilized_trials[i],
                                                 self.utilized_trials[j]))
                            
                # Permutations is a list of 90 elements, each element contains
                # two dictionaries. The first dictionary will be on the left,
                # the second dictionary on the right. In order to make things 
                # a bit more clear, we convert this permutations list to a 
                # list of dictionaries, each one containing clear metadata for
                # each trial including: left assignment, right assignment, 
                # trial type ("PvP", "PvC", "CvC"), trial number...
                # For example:
                # {'left': {'Name': 'Probe1.jpg', 'TrainingSet': '0', 'StimulusNum': '1'},
                #  'right': {'Name': 'Probe2.jpg', 'TrainingSet': '0', 'StimulusNum': '2'},
                #  'trial_type': 'PvP'}
                
                self.trial_meta_data_list = []
                for t in permutations:
                    left = t[0]
                    right = t[1]
                    # Determine trial type
                    if left['TrainingSet'] == '0' and right['TrainingSet'] == '0':
                        trial_type = 'PvP'
                    elif left['TrainingSet'] == right['TrainingSet']:
                        trial_type = 'CvC'
                    else:
                        trial_type = 'PvC'
                    # Load in image files
                    # Assign metadata to new list
                    e =  {'left': left,
                          'right': right,
                          'trial_type': trial_type}
                    self.trial_meta_data_list.append(e)
                    
                # Quasi-randomly shuffle trials such that there are no repeats 
                # of stimuli
                while True:
                    bad_shuffle = False # Innocent until proven otherwise
                    list_of_trials = deepcopy(self.trial_meta_data_list) # Copy previous list so that we can remove/pop items
                    shuffle(list_of_trials)
                    rec_counter = 0
                    self.trial_stimulus_order = []
                    while True:
                        # Two end conditions
                        if len(list_of_trials) == 1:
                            self.trial_stimulus_order.append(list_of_trials[0])
                            break
                        
                        if rec_counter > 20: # Start over if too many recursions
                            bad_shuffle = True
                            break
                        
                        l1 = list_of_trials[0]["left"]["Name"]
                        r1 = list_of_trials[0]["right"]["Name"]
                        l2 = list_of_trials[1]["left"]["Name"]
                        r2 = list_of_trials[1]["right"]["Name"]
                        
                        if len([l1, r1, l2, r2]) != len(set([l1, r1, l2, r2])): 
                            i1 = list_of_trials.pop(0)
                            shuffle(list_of_trials)
                            list_of_trials.insert(0, i1)
                            rec_counter += 1
                            
                        else: # If no matches, we can preserve the previous pair
                            self.trial_stimulus_order.append(list_of_trials.pop(0))
                            rec_counter = 0
                            
                    # Break if good shuffle
                    if bad_shuffle == False:
                        break # Break while loop
                        
                # Finally, load the image files into the dictionary:
                for i in self.trial_stimulus_order:
                    i["left"]["img"] = ImageTk.PhotoImage(Image.open(f'P039a_Stimuli/{i["left"]["Name"]}'))
                    i["right"]["img"] = ImageTk.PhotoImage(Image.open(f'P039a_Stimuli/{i["right"]["Name"]}'))
            
            # After the order of stimuli per trial is determined, there are a 
            # couple other things that neeed to occur during the first ITI:
            if self.subject_ID == "TEST": # If test, don't worry about ITI delays
                self.ITI_duration = 5 * 1000
                self.hopper_duration = 2 * 1000
                self.trial_delay_duration = 1 * 1000
                self.root.after(1, lambda: self.ITI())
            else:
                self.root.after(60000, lambda: self.ITI())
                
        ### hopper_light_GPIO_num
        if self.record_video:
            record_str = "ON"
        else:
            record_str = "OFF"
            
        self.root.bind("<space>", first_ITI) # bind cursor state to "space" key
        self.mastercanvas.create_text(512,374,
                                      fill="white",
                                      font="Times 25 italic bold",
                                      text=f" Place bird in box, then press space\n\n Experiment: P039a  \n Subject: {self.subject_ID} \n Training Phase {self.training_phase_name_list[self.training_phase]} \n Cameras: {record_str}")
    
    ## Video recording functions to start and stop recording from both top and side both cameras
    
    def start_recording_video(self):
        current_date = strftime("%Y-%m-%d")  # Format: YYYYMMDD
        base_filename = f"{self.subject_ID}_Phase{self.training_phase}_{current_date}_Trial{self.trial_num}-{self.trial_type}"
        subject_folder_directory = f"Desktop/Videos/{self.subject_ID}"
        
        self.top_filename  = f"{base_filename}_TOPcam.mp4"
        self.side_filename = f"{base_filename}_SIDEcam.mp4"
        
        # Make subject folder if it doesn't already exist
        try:
            mkdir(str(os_path.expanduser('~')) + "/" + subject_folder_directory)
        except FileExistsError:
            pass
        
        #Start recording with the generated filenames
        run([
            "./start_recording.sh",
            f"{subject_folder_directory}/{self.top_filename}",
            f"{subject_folder_directory}/{self.side_filename}"
        ])
        self.currently_recording = True
        self.write_data(None,"video_recording_started")
        
    
    def stop_recording_video(self):
        run([
            "./stop_recording.sh",
            str(self.trial_num)
        ])
        self.currently_recording = False
        self.write_data(None,"video_recording_stopped")
    
            
    
    ## %% ITI
    # Every trial (including the first) "starts" with an ITI. The ITI function
    # does several different things:
    #   1) Checks to see if any session constraints have been reached (and ends the session if so)
    #   2) Resets the hopper and any trial-by-trial variables (including RRs)
    #   3) Increases the trial counter by one
    #   4) Moves on to the next trial after a delay
    # 
    def ITI (self):
        # This function just clear the screen. It will be used a lot in the future, too.
        self.clear_canvas()
        
        # Make sure pecks during ITI are saved
        self.mastercanvas.create_rectangle(0,0,
                                           self.mainscreen_width,
                                           self.mainscreen_height,
                                           fill = "black",
                                           outline = "black",
                                           tag = "bkgrd")
        self.mastercanvas.tag_bind("bkgrd",
                                   "<Button-1>",
                                   lambda event, 
                                   event_type = "ITI_peck": 
                                       self.write_data(event, event_type))
            
        # Stop recording if we were recording
        if self.currently_recording:
            self.stop_recording_video()
            self.top_filename  = "NA"
            self.side_filename = "NA"
        
        # First, check to see if any session limits have been reached (e.g.,
        # if the max time or reinforcers earned limits are reached).
        if self.trial_num > self.max_number_of_reinforced_trials: # Maybe -1 (89)>
            print("Trial max reached")
            self.exit_program("TrialsCompleted")
            
        # elif datetime.now() >= (self.session_duration):
        #    print("Time max reached")
        #    self.exit_program("TimeCompleted")
        
        # Else, after a timer move on to the next trial. Note that,
        # although the after() function is given here, the rest of the code 
        # within this function is still executed before moving on.
        else: 
            # Print text on screen if a test (should be black if an experimental trial)
            if not operant_box_version or self.subject_ID == "TEST":
                self.mastercanvas.create_text(512,374,
                                              fill="white",
                                              font="Times 25 italic bold",
                                              text=f"ITI ({int(self.ITI_duration/1000)} sec.)")
                
            # This turns all the stimuli off from the previous trial (during the
            # ITI).
            if operant_box_version:
                rpi_board.write(hopper_light_GPIO_num,
                                False) # Turn off the hopper light
                rpi_board.set_servo_pulsewidth(servo_GPIO_num,
                                               hopper_down_val) # Hopper down
                rpi_board.write(house_light_GPIO_num, 
                                False) # Turn off house light
                # Stop recording
                
            # Reset other variables for the following trial.
            self.trial_start = time() # Set trial start time (note that it includes the ITI, which is subtracted later)
            self.trial_substage_start_time = time() # Reset substage timer
            self.write_comp_data(False) # update data .csv with trial data from the previous trial
            self.trial_stage = 1 # Reset trial substage
            
            if self.training_phase != 0: # If trials differ, grab info for upcoming trial
                self.trial_info = self.trial_stimulus_order[self.trial_num]
                self.trial_type = self.trial_info['trial_type']

            # Increase trial counter by one
            self.trial_num += 1
            
            # Setup variable ITI and RR
            if self.training_phase in [0,1]:
                self.ITI_duration    = choice(list(range(10,21))) * 1000
                self.trial_RR        = choice(list(range(3, 8))) # RR5
                self.button_presses  = 0
                
            elif self.training_phase == 2:
                self.ITI_duration    = 20 * 1000
                # Choice Task RR
                self.choice_trial_RR       = 10 # RR10
                self.left_button_presses   = 0
                self.right_button_presses  = 0
                # Terminal link RR
                # Terminal link RR
                self.terminal_link_trial_RR = choice(list(range(7, 13))) # RR10
                self.terminal_link_button_presses = 0
                
            if self.subject_ID == "TEST":
                self.ITI_duration = 1 * 1000
            
            #Start recording function for choice task (during ITI)
            def start_recording_ITI():
                self.start_recording_video()
                self.root.after(3*1000, self.sub_stage_one)
                
            # Next, set a delay timer to proceed to the next trial
            if self.record_video and self.training_phase == 2:
                self.root.after((self.ITI_duration - 3*1000), start_recording_ITI)
            else: 
                self.root.after(self.ITI_duration, self.sub_stage_one)
                
            # Finally, print terminal feedback "headers" for each event within the next trial
            print(f"\n{'*'*30} Trial {self.trial_num} begins {'*'*30}") # Terminal feedback...
            print(f"{'Event Type':>30} | Xcord.   Ycord. | Stage | Session Time")
        
    #%%  Pre-choice loop 
    """
    Each trial is built of a series of seperate stages (following the ITI). The
    pre-training and mixed instrumental-autoshaping procedures each use a subset
    of three stages (Blank screen/trial start, )
    
    The numeric "code" of ...
    each stage is given below, and are used in the "build_keys()" function 
    below to determine what keys should be colored and activated.
    
    Choice phase has 4 sub-stages: 
    
    TO-DO: fill in this description of how the trial runs and substages work
    
    Substage 1: The canvas is made blank, house light turned on, and video 
    recording of trial starts and the file name is saved
    

    """
    def sub_stage_one(self):
        self.clear_canvas()
        self.trial_substage_start_time = time()
        self.trial_stage = 1
        if operant_box_version:
            rpi_board.write(house_light_GPIO_num,
                            True) # Turn on the houselight
            if self.record_video and self.training_phase in [0,1]:  # Video recording for 2 starts during ITI
                self.start_recording_video()
        self.build_keys()
        if self.training_phase in [0,1]:
            self.root.after(self.trial_delay_duration, self.sub_stage_two)
        
        
    def sub_stage_two(self):
        self.trial_substage_start_time = time()
        self.trial_stage = 2
        self.build_keys()
        if self.training_phase in [0,1]:
            self.auto_timer = self.root.after(self.auto_reinforcer_timer,
                                              lambda: self.provide_food(False)) # False b/c non autoreinforced
    
        
    def build_keys(self):
        # This is a function that builds the all the buttons on the Tkinter
        # Canvas. The Tkinter code (and geometry) may appear a little dense
        # here, but it follows many of the same rules. All keys will be built
        # during non-ITI intervals, but they will only be filled in and active
        # during specific times. However, pecks to keys will be differentiated
        # regardless of activity.
        
        # First, build the background. This basically builds a button the size of 
        # screen to track any pecks; buttons built on top of this button will
        # NOT count as background pecks but as key pecks, because the object is
        # covering that part of the background. Once a peck is made, an event line
        # is appended to the data matrix.
        self.mastercanvas.create_rectangle(0,0,
                                           self.mainscreen_width,
                                           self.mainscreen_height,
                                           fill = "#7F7F7F", #"red", 
                                           outline = "#7F7F7F",
                                           tag = "bkgrd")
        self.mastercanvas.tag_bind("bkgrd",
                                   "<Button-1>",
                                   lambda event, 
                                   event_type = "background_peck": 
                                       self.write_data(event, event_type))
        # Pre-training
        if self.training_phase == 0 and self.trial_stage == 2:
            # Build our pre-training nesting oval stimuli
            self.mastercanvas.create_oval(392, 258, 609, 475,
                                          fill = "#7F7F7F",
                                          outline = "",
                                          tag = "pretraining_key")
            
            self.mastercanvas.create_oval(417, 283, 584, 450,
                                          fill      = "#2596be",
                                          outline   = "black",
                                          tag       = "pretraining_key")
            
            self.mastercanvas.create_oval(500, 365, 502, 367,
                                          fill      = "black",
                                          outline   = "black",
                                          tag       = "pretraining_key")
            
            self.mastercanvas.tag_bind("pretraining_key",
                                       "<Button-1>",
                                       lambda event,
                                       ks = "pretraining_key": self.key_press(event,
                                                                    ks))
        # Mixed-autoshaping
        if self.training_phase == 1 and self.trial_stage == 2:
                # COMPLETED: Receptive field should encompass all shapes (350p diameter rn)
                self.mastercanvas.create_oval(189, 129, 832, 639,
                                              fill      = "#7F7F7F",
                                              outline   = "#7F7F7F", #"#7F7F7F" Add grey...
                                              width     = 1, 
                                              tag       = "stimulus_key")
                
                #Build the image on top of receptive field
                self.mastercanvas.create_image(*self.image_center,
                                               anchor ='center',
                                               image  = self.trial_info["img"],
                                               tag    = "stimulus_key"
                                               )
                
               
                
                self.mastercanvas.tag_bind("stimulus_key",
                                           "<Button-1>",
                                           lambda event,
                                           ks = "stimulus_key": self.key_press(event,
                                                                        ks))
        # Choice phase
        elif self.training_phase == 2:
            # Binary choice sub-phase 1
            if self.trial_stage == 1:
                # Setup l/r coordinate and image info
                left_key_data = self.trial_info['left']
                right_key_data = self.trial_info['right']
                
                # Left image
                self.mastercanvas.create_image(*self.choice_key_coord_dict["left_choice"],
                                               anchor   = 'center',
                                               image    = left_key_data["img"],
                                               tag      = "left_stimulus_key" # Because receptive field will manage outcome
                                               )
                # Right image
                self.mastercanvas.create_image(*self.choice_key_coord_dict["right_choice"],
                                               anchor   = 'center',
                                               image    = right_key_data["img"],
                                               tag      = "right_stimulus_key"
                                               )
                # Reset background
                self.mastercanvas.tag_bind("bkgrd",
                                           "<Button-1>",
                                           lambda event, 
                                           event_type = "background_peck": 
                                               self.write_data(event, event_type))
                    
                
                ## Setup tagged functions
                self.mastercanvas.tag_bind("left_stimulus_key",
                                           "<Button-1>",
                                           lambda event,
                                           ks = "left_stimulus_key": self.key_press(event,
                                                                        ks))
                
                self.mastercanvas.tag_bind("right_stimulus_key",
                                           "<Button-1>",
                                           lambda event,
                                           ks = "right_stimulus_key": self.key_press(event,
                                                                        ks))

                
            if self.trial_stage == 2:
                # Build our terminal link oval stimuli
                self.mastercanvas.create_oval(392, 258, 609, 475,
                                              fill = "#7F7F7F",
                                              outline = "",
                                              tag = "terminallink_key")
                
                self.mastercanvas.create_oval(417, 283, 584, 450,
                                              fill = "#D5869D",
                                              outline = "black",
                                              tag = "terminallink_key")
                
                self.mastercanvas.create_oval(500, 365, 502, 367,
                                              fill = "black",
                                              outline = "black",
                                              tag = "terminallink_key")
                
                self.mastercanvas.tag_bind("terminallink_key",
                                           "<Button-1>",
                                           lambda event,
                                           ks = "terminallink_key": self.key_press(event,
                                                                        ks))
            
    """ 
    # COMPLETED: Explain what key_press() function does
    
    This key_press() function is responsible for registering pigeon inputs when
    the "receptive fields" for each training phases is pecked on. For the 
    pre-training and mixed autoshaping-instrumental phases, the function would
    retreive the type of input (stimulus or background), and register the 
    coordinates of this respective input as well. Additionally, it would 
    keep a counter of "button presses", in order for us to apply the correct
    reinforcement schedule. For the choice task, this logic was maintained, but
    the inputs were now registered as either "left_stimulus_key" or 
    "right_stimulus_key", and this reinforcement schedule was then applied once 
    again. Succeeding this, the terminal link would appear on the screen and
    the key_press() function would apply itself once again in order to ensure 
    the correct reinforcement schedule for this terminal link subphase. 
    
    """
    
    def key_press(self, event, keytag):
        # For pre-training and mixed autoshaping-instrumental
        if self.training_phase in [0, 1]:
            self.write_data(event, (f"{keytag}_peck"))
            self.button_presses += 1 
            if self.button_presses == self.trial_RR:
                # Next, cancel the timer (if it exists)
                try:
                    self.root.after_cancel(self.auto_timer)
                except AttributeError:
                    pass
                self.provide_food(True)

        # For binary choice trials 
        elif self.training_phase == 2:
            # Choice subphase 1
            if self.trial_stage == 1:
                self.write_data(event, (f"{keytag}_peck"))
                if keytag == "left_stimulus_key":
                    self.left_button_presses += 1
                elif keytag == "right_stimulus_key":
                    self.right_button_presses += 1
                # Check if RR has been reached 
                if self.left_button_presses == self.choice_trial_RR:
                    self.write_data(event, ("left_stimulus_choice"))
                    self.write_data(event, (f"{self.trial_info['left']['Name'].split('.')[0]}_choice"))
                    self.sub_stage_two()
                elif self.right_button_presses == self.choice_trial_RR:
                    self.write_data(event, ("right_stimulus_choice"))
                    self.write_data(event, (f"{self.trial_info['left']['Name'].split('.')[0]}_choice"))
                    self.sub_stage_two()
            # Terminal link subphase 2
            elif self.trial_stage == 2:
                self.write_data(event, (f"{keytag}_peck"))
                self.terminal_link_button_presses += 1
                # Check if RR has been reached 
                if self.terminal_link_button_presses == self.terminal_link_trial_RR:
                    self.write_data(event, ("terminal_link_completed"))
                    self.provide_food(True)

        
    
    # %% Post-choice contingencies: always either reinforcement (provide_food)
    # or time-out (time_out_func). Both lead back to the next trial's ITI,
    # thereby completing the loop.
    
    def provide_food(self, key_pecked):
        # This function is contingent upon correct and timely choice key
        # response. It opens the hopper and then leads to ITI after a preset
        # reinforcement interval (i.e., hopper down duration)
        self.clear_canvas()
        
        # If key is operantly reinforcedhopper_light_GPIO_num
        if key_pecked:
            self.write_data(None, "reinforcer_provided")
            if not operant_box_version or self.subject_ID == "TEST":
                self.mastercanvas.create_text(512,374,
                                              fill="white",
                                              font="Times 25 italic bold", 
                                              text=f"Key Pecked \nFood accessible ({int(self.hopper_duration/1000)} s)") # just onscreen feedback
        else: # If auto-reinforced
            self.write_data(None, "auto_reinforcer_provided")
            if not operant_box_version or self.subject_ID == "TEST":
                    self.mastercanvas.create_text(512,374,
                                  fill="White",
                                  font="Times 25 italic bold", 
                                  text=f"Auto-timer complete \nFood accessible ({int(self.hopper_duration/1000)} s)") # just onscreen feedback

        # Next send output to the box's hardware
        if operant_box_version:
            rpi_board.write(house_light_GPIO_num,
                            False) # Turn off the house light
            rpi_board.write(hopper_light_GPIO_num,
                            True) # Turn off the house light
            rpi_board.set_servo_pulsewidth(servo_GPIO_num,
                                           hopper_up_val) # Move hopper to up position
            
        ITI_timer = self.root.after(self.hopper_duration, lambda: self.ITI())
        

    # %% Outside of the main loop functions, there are several additional
    # repeated functions that are called either outside of the loop or 
    # multiple times across phases.
    
    def change_cursor_state(self):
        # This function toggles the cursor state on/off. 
        # May need to update accessibility settings on your machince.
        if self.cursor_visible: # If cursor currently on...
            self.root.config(cursor="none") # Turn off cursor
            print("### Cursor turned off ###")
            self.cursor_visible = False
        else: # If cursor currently off...
            self.root.config(cursor="") # Turn on cursor
            print("### Cursor turned on ###")
            self.cursor_visible = True
    
    def clear_canvas(self):
         # This is by far the most called function across the program. It
         # deletes all the objects currently on the Canvas. A finer point to 
         # note here is that objects still exist onscreen if they are covered
         # up (rendering them invisible and inaccessible); if too many objects
         # are stacked upon each other, it can may be too difficult to track/
         # project at once (especially if many of the objects have functions 
         # tied to them. Therefore, its important to frequently clean up the 
         # Canvas by literally deleting every element.
        try:
            self.mastercanvas.delete("all")
        except TclError:
            print("No screen to exit")
        
    def exit_program(self, event): 
        # This function can be called two different ways: automatically (when
        # time/reinforcer session constraints are reached) or manually (via the
        # "End Program" button in the control panel or bound "esc" key).
            
        # The program does a few different things:
        #   1) Return hopper to down state, in case session was manually ended
        #       during reinforcement (it shouldn't be)
        #   2) Turn cursor back on
        #   3) Writes compiled data matrix to a .csv file 
        #   4) Build a black screen until manually exited
        def other_exit_funcs():
            if operant_box_version:
                rpi_board.write(hopper_light_GPIO_num,
                                False) # turn off hopper light
                rpi_board.write(house_light_GPIO_num,
                                False) # Turn off the house light
                rpi_board.write(string_LED_GPIO_num,
                                False) # Turn off the LED lights
                rpi_board.set_servo_pulsewidth(servo_GPIO_num,
                                               hopper_down_val) # set hopper to down state
                sleep(1) # Sleep for 1 s
                rpi_board.set_PWM_dutycycle(servo_GPIO_num,
                                            False)
                rpi_board.set_PWM_frequency(servo_GPIO_num,
                                            False)
                rpi_board.stop() # Kill RPi board
                
                # Next, cancel the timer (if it exists)
                try:
                    self.root.after_cancel(self.auto_timer)
                    self.root.after_cancel(self.ITI_timer)
                except AttributeError:
                    pass

                if not self.cursor_visible:
                    	self.change_cursor_state() # turn cursor back on, if applicable
                        
                if self.record_video and self.currently_recording:
                    self.stop_recording_video()
                    
            self.write_comp_data(True) # write data for end of session
            
            if event not in ["TrialsCompleted", "TimeCompleted"]: # If not, black screen by default
                self.root.destroy() # destroy Canvas
            
            print("\n GUI window exited")
            
        self.clear_canvas()
        other_exit_funcs()
        print("\n You may now exit the terminal and operater windows now.")
        
    
    def write_data(self, event, outcome):
        # This function writes a new data line after EVERY peck. Data is
        # organized into a matrix (just a list/vector with two dimensions,
        # similar to a table). This matrix is appended to throughout the 
        # session, then written to a .csv once at the end of the session.
        
        # First generate spatial info
        if event != None: 
            x, y = event.x, event.y
            # Distance from center of stimuli
            if self.training_phase in [0,1]:
                center_pyth_distance  = ((x - self.image_center[0]) ** 2 + (y - self.image_center[1]) ** 2) ** 0.5
                left_pyth_dist, right_pyth_dist = "NA", "NA"
            elif self.training_phase == 2:
                center_pyth_distance   = ((x - self.image_center[0]) ** 2 + (y - self.image_center[1]) ** 2) ** 0.5
                left_pyth_dist         = ((x - self.choice_key_coord_dict["left_choice"][0]) ** 2 + (y - self.choice_key_coord_dict["left_choice"][1]) ** 2) ** 0.5       
                right_pyth_dist        = ((x - self.choice_key_coord_dict["right_choice"][0]) ** 2 + (y - self.choice_key_coord_dict["right_choice"][1]) ** 2) ** 0.5   
        else: # There are certain data events that are not pecks.
            x, y, center_pyth_distance, left_pyth_dist, right_pyth_dist = "NA", "NA", "NA", "NA", "NA"
        
        # Next document stimuli used 
        if self.training_phase == 0:
            center_stimulus = "control_circle"
            trial_type = "pretraining"
            left_stim, left_stim_training_set, left_stim_num = "NA", "NA", "NA"
            right_stim, right_stim_training_set, right_stim_num = "NA", "NA", "NA"
            subphase1_RR, subphase1_left_button_presses, subphase1_right_button_presses = "NA", "NA", "NA"
            subphase2_RR = self.trial_RR 
            subphase2_button_presses = self.button_presses
            
        elif self.training_phase == 1:
            trial_type      = self.trial_info['trial_type']
            center_stimulus = self.trial_info["Name"].split(".")[0]
            left_stim, left_stim_training_set, left_stim_num = "NA", "NA", "NA"
            right_stim, right_stim_training_set, right_stim_num = "NA", "NA", "NA"
            subphase1_RR, subphase1_left_button_presses, subphase1_right_button_presses = "NA", "NA", "NA"
            subphase2_RR = self.trial_RR 
            subphase2_button_presses = self.button_presses
                
        elif self.training_phase == 2:
            # Stimuli
            trial_type              = self.trial_info['trial_type']
            center_stimulus         = "terminal_link_circle"
            left_stim               = self.trial_info["left"]["Name"].split(".")[0]
            left_stim_training_set  = self.trial_info["left"]["TrainingSet"]
            left_stim_num           = self.trial_info["left"]["StimulusNum"]
            right_stim              = self.trial_info["right"]["Name"].split(".")[0]
            right_stim_training_set = self.trial_info["right"]["TrainingSet"]
            right_stim_num          = self.trial_info["right"]["StimulusNum"]
            # Button presses
            subphase1_RR = self.choice_trial_RR
            subphase1_left_button_presses = self.left_button_presses
            subphase1_right_button_presses = self.right_button_presses
            subphase2_RR = self.terminal_link_trial_RR 
            subphase2_button_presses = self.terminal_link_button_presses
            
        # Print terminal feedback
        print(f"{outcome:>30} | x: {x: ^4} y: {y:^4} | {self.trial_stage:^5} | {str(datetime.now() - self.start_time)}")
        
        self.session_data_frame.append([
            
            # First data that allows us to ID the file
            self.subject_ID, # Name of subject (same across datasheet)
            date.today(), # Today's date as "MM-DD-YYYY"
            self.training_phase, # the phase of training as a number (0-2)
            self.training_phase_name_list[self.training_phase].split(": ")[1], # Training phase name 
            
            # Then important within-session data
            str(datetime.now() - self.start_time), # SessionTime as datetime object
            self.trial_num, # Trial count within session (1 - max # trials)
            trial_type, # Trial type
            outcome, # Type of event (e.g., background peck, target presentation, session end, etc.)
            
            # Temporal info
            self.trial_stage, # Substage within each trial (1-2)
            round((time() - self.trial_start - (self.ITI_duration/1000)), 5), # Time into this trial minus ITI (if session ends during ITI, will be negative)
            round((time() - self.trial_substage_start_time), 5), # Trial substage timer
            self.ITI_duration,  # ITI differs 
            
            # Spatial peck info 
            x, # X coordinate of a peck
            y, # Y coordinate of a peck
            center_pyth_distance, # Pythagorean dist. b/n center stimulus and this peck
            left_pyth_dist, # Pythagorean dist. b/n left choice stimulus and this peck
            right_pyth_dist, # Pythagorean dist. b/n right choice stimulus and this peck

            # Stimuli used w/ independent responses
            center_stimulus,
            left_stim,
            left_stim_training_set,
            left_stim_num,
            right_stim,
            right_stim_training_set, 
            right_stim_num, 
            
            # Button press info
            subphase1_RR,
            subphase1_left_button_presses,
            subphase1_right_button_presses,
            subphase2_RR,
            subphase2_button_presses,
            
            # Video info
            self.record_video, # Video recording 0/1
            self.top_filename, # Recording file name
            self.side_filename # Recording file name
            ])
        
        # Repeated here to double-check
        header_list = ["Subject", "Date", "ExpPhaseNum", "ExpPhaseName", 
                       "SessionTime", "TrialNum", "TrialType", "EventType",
                       "TrialSubStage", "TrialTime", "TrialSubStageTimer",
                       "ITIDuration", "Xcord","Ycord", "CenterPythDist", 
                       "LeftPythDist", "RightPythDist", "CenterStim",
                       "LeftStim", "LeftStimTrainingSet", "LeftStimNumber",
                       "RightStim", "RightStimTrainingSet", "RightStimNumber",
                       "SubPhase1RR", "SubPhase1LeftButtonPresses",
                       "SubPhase1RightButtonPresses", "SubPhase2RR",
                       "SubPhase2ButtonPresses", "VideoRecorded",
                       "TopVideoFileName", "SideVideoFileName"]

        
    def write_comp_data(self, SessionEnded):
        # The following function creates a .csv data document. It is either 
        # called after each trial during the ITI (SessionEnded ==False) or 
        # one the session finishes (SessionEnded). If the first time the 
        # function is called, it will produce a new .csv out of the
        # session_data_matrix variable, named after the subject, date, and
        # training phase. Consecutive iterations of the function will simply
        # write over the existing document.
        if SessionEnded:
            self.write_data(None, "SessionEnds") # Writes end of session to df
        if self.record_data : # If experimenter has choosen to automatically record data in seperate sheet:
            myFile_loc = f"{self.data_folder_directory}/{self.subject_ID}/{self.subject_ID}_{self.start_time.strftime('%Y-%m-%d_%H.%M.%S')}_P034b_data-Phase{self.training_phase}.csv" # location of written .csv
            # This loop writes the data in the matrix to the .csv              
            edit_myFile = open(myFile_loc, 'w', newline='')
            with edit_myFile as myFile:
                w = writer(myFile, quoting=QUOTE_MINIMAL)
                w.writerows(self.session_data_frame) # Write all event/trial data 
            print(f"\n- Data file written to {myFile_loc}")
                
#%% Finally, this is the code that actually runs:
try:   
    if __name__ == '__main__':
        cp = ExperimenterControlPanel()
except:
    # If an unexpected error, make sure to clean up the GPIO board
    if operant_box_version:
        rpi_board.set_PWM_dutycycle(servo_GPIO_num,
                                    False)
        rpi_board.set_PWM_frequency(servo_GPIO_num,
                                    False)
        rpi_board.stop()
        # Stop command to video recording if the program crashes
        if self.record_video and self.currently_recording:
            self.stop_recording_video()
            
            

