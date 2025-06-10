from tkinter import *
from PIL import ImageTk, Image
from functools import partial
import csv
import random

# Global Variables
big_font = ("B612", "16", "bold")
med_font = ("B612", "12")
med_fontb = ("B612", "12", "bold")
small_font = ("B612", "10")
small_fontb = ("B612", "10", "bold")

# Global Functions Here
def get_csv_data():
    """
    Gets data from the csv file.
    Returns: list of aircraft where each item has the 
    name, type, workplace, and image file name
    """
    file = open("Aircraft Quiz/Aircraft Data/00_aircraft.csv", "r")
    all_aircraft = list(csv.reader(file, delimiter=","))
    file.close()

    # Remove the first row (header) from the list
    all_aircraft.pop(0)

    return all_aircraft


class StartGame():
    """
    Aircraft Quiz Start Game Screen
    """

    def __init__(self):
        """
        Start Game GUI
        """
        # Make it so the windows close button actually closes the quiz
        root.protocol('WM_DELETE_WINDOW', root.destroy)

        # Setup for radiobuttons
        self.imgname_filt = StringVar()
        self.planeheli_filt = StringVar()
        self.civmil_filt = StringVar()

        # Long strings
        main_instructions = "Select the filter options and enter the number of rounds\nyou want below or Click Here"
        self.round_instructions = "Please enter the # of rounds\n you want to be quizzed on."

        # Setup required for Background
        bg_path = "C:/Users/scrap/OneDrive - Massey High School/Year 13 (2025)/TCCOUE/Aircraft Quiz/Documentation/aircraft_background.jpg"  # Use correct relative path
        bg_img = Image.open(bg_path)
        resize_img = bg_img.resize((500, 720), Image.Resampling.LANCZOS)  # Resize to fit window
        self.bg_img = ImageTk.PhotoImage(resize_img)

        # Label Containing the Background
        self.start_bg = Label(root, image=self.bg_img)
        self.start_bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.start_bg.image = self.bg_img

        # Main Heading Title of Window
        self.start_heading = Label(root, text="Welcome To\nThe Best Aircraft Quiz",
                                   font=("B612", "16", "bold"), width=22, border=1, relief="solid")
        self.start_heading.place(x=105, y=20)

        # Main Quiz Instructions
        self.start_instruct = Button(root, text=main_instructions, command=self.to_instructions,
                                   font=("B612", "10", "bold"), width=50, height=2, border=1, relief="solid")
        self.start_instruct.place(x=50, y=115)

        # Image or Name Filter Frame
        self.in_filt_frame = Frame(root)
        self.in_filt_frame.place(x=140, y=215)
        self.imgname_filt.set(0)
 
        # Plane, Heli Filter Frame
        self.ph_filt_frame = Frame(root)
        self.ph_filt_frame.place(x=140, y=285)
        self.planeheli_filt.set(0)

        # Civ, Mil Filter Frame
        self.cm_filt_frame = Frame(root)
        self.cm_filt_frame.place(x=140, y=355)
        self.civmil_filt.set(0)

        # List for holding label details (Frame | Text | Variable | Value | Width | Column)
        start_radio_list = [
            [self.in_filt_frame, "Quiz The Image", self.imgname_filt, 0, 13, 0],
            [self.in_filt_frame, "Quiz The Name", self.imgname_filt, 1, 13, 1],
            [self.ph_filt_frame, "Plane", self.planeheli_filt, 1, 9, 0],
            [self.ph_filt_frame, "Both", self.planeheli_filt, 0, 7, 1],
            [self.ph_filt_frame, "Helicopter", self.planeheli_filt, 2, 9, 2],
            [self.cm_filt_frame, "Civilian", self.civmil_filt, 1, 9, 0],
            [self.cm_filt_frame, "Both", self.civmil_filt, 0, 7, 1],
            [self.cm_filt_frame, "Military", self.civmil_filt, 2, 9, 2]
        ]

        # List to hold labels once they have been made
        self.radios_ref_list = []

        # Loop through every item in label list to make label
        for item in start_radio_list:
            self.make_radio = Radiobutton(item[0], text=item[1], variable=item[2], value=item[3], width=item[4],
                                          font=("B612", "10"), bg="#aaaacc", selectcolor="#dddddd", height=2, border=1, relief="solid", indicatoron=0)
            self.make_radio.grid(row=0, column=item[5])
            self.radios_ref_list.append(self.make_radio)

        # Ask user quiz rounds
        self.round_instruct = Label(root, text=self.round_instructions,
                                   font=("B612", "10", "bold"), width=28, height=2, border=1, relief="solid")
        self.round_instruct.place(x=138, y=500)

        self.round_entry = Entry(root, font=("B612", "16"), width=17, border=1, relief="solid", justify="center")
        self.round_entry.place(x=139, y=550)

        # End & Start Game Buttons
        self.end_game_but = Button(root, text="🚫 End Quiz 🚫", command=root.destroy,
                                   font=("B612", "16", "bold"), width=13, border=1, relief="solid")
        self.end_game_but.place(x=30, y=650)

        self.start_game_but = Button(root, text="✅ Play Quiz ✅", command=self.check_rounds,
                                     font=("B612", "16", "bold"), width=13, border=1, relief="solid")
        self.start_game_but.place(x=295, y=650)

    def check_rounds(self):
        """
        Checks whether users input for rounds is valid
        """
        # Retrieve temperature to be converted
        rounds_wanted = self.round_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.round_instruct.config(fg="#000000", text=self.round_instructions, font=small_fontb)
        self.round_entry.config(bg="#ffffff")

        error = "Oops - Please choose a whole number between 0 and 1000."
        has_errors = "no"

        # Checks that amount to be converted is a number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0 and rounds_wanted < 1000:
                # Invoke Play Class (and take across number of rounds)
                aircraft_list = self.filter_aircraft(self.imgname_filt, self.planeheli_filt, self.civmil_filt)
                Play(rounds_wanted, self.imgname_filter, self.ph_filt, self.cm_filt, aircraft_list)
                # Reset Start Game Window for if user returns
                self.round_entry.delete(0, END)

                # Hide Root Window (ie: hide rounds choice window)
                root.withdraw()
            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # Display the error if necessary
        if has_errors == "yes":
            # Re-enable start game button if error occurs
            self.start_game_but.config(state=NORMAL)
            # Change label and entry box to show error
            self.round_instruct.config(text=error, fg="#990000", font=small_fontb, wraplength=200)
            self.round_entry.config(bg="#f4cccc")
            self.round_entry.delete(0, END)

    def filter_aircraft(self, imgname, filt1, filt2):
        """
        Takes the list of aircraft and filters it based on the filters chosen by the user.
        Returns: list of aircraft that match the filters chosen by the user
        """
        # Get full aircraft list
        all_aircraft = get_csv_data()

        # Get the filters chosen by the user
        ph_filt = filt1.get()
        if ph_filt == "1":
            self.ph_filt = "Plane"
        elif ph_filt == "2":
            self.ph_filt = "Helicopter"
        else:
            self.ph_filt = "Both"
        cm_filt = filt2.get()
        if cm_filt == "1":
            self.cm_filt = "Civilian"
        elif cm_filt == "2":
            self.cm_filt = "Military"
        else:
            self.cm_filt = "Both"

        imgname_filt = imgname.get()
        if imgname_filt == "0":
            self.imgname_filter = "Image"
        else:
            self.imgname_filter = "Name"

        # Lists for sorting filtered aircraft
        planeheli_aircraft = []
        filtered_aircraft = []

        # Filter the list of aircraft based on the filters chosen by the user
        for aircraft in all_aircraft:
            # If filter is 'Both' just all all aircraft to list
            if self.ph_filt == "Both":
                planeheli_aircraft.append(aircraft)
            # If filter isn't 'Both' then only add aircraft with corresponding type
            else:
                if aircraft[1] == self.ph_filt:
                    planeheli_aircraft.append(aircraft)
                
        # Civlian/Military Filter work
        for aircraft in planeheli_aircraft:
            # If filter is 'Both' just all all aircraft to list
            if self.cm_filt == "Both":
                filtered_aircraft.append(aircraft)
            # If filter isn't 'Both' then only add aircraft with corresponding type
            else:
                if aircraft[2] == self.cm_filt:
                    filtered_aircraft.append(aircraft)

        # Reset Option Buttons
        self.imgname_filt.set(0)
        self.planeheli_filt.set(0)
        self.civmil_filt.set(0)

        return filtered_aircraft

    def to_instructions(self):
        """
        Displays instructions for playing game
        """
        # Disables instrucions, end and start game button to be used again
        self.start_instruct.config(state=DISABLED)
        self.end_game_but.config(state=DISABLED)
        self.start_game_but.config(state=DISABLED)

        DisplayInstructions(self)

    def end_quiz(self):
        # Destroys the root window, start game
        root.destroy()


class Play():
    """
    Interface for playing the Aircraft Quiz
    """

    def __init__(self, how_many, imgname, filt1, filt2, filtered_aircraft):
        """
        Sets many variables and creates the main GUI for the Play window
        """
        # Set filters for better looks
        if filt1 == "Both" and filt2 == "Both":
            self.filter1 = "EVERYTHING"
            self.filter2 = ""
        else:
            self.filter1 = filt1
            self.filter2 = f"& '{filt2}'"
        
        # Game Variables
        self.rounds_played = 0

        self.rounds_wanted = how_many

        self.rounds_won = 0

        self.filtered_aircraft = filtered_aircraft

        self.imgname = imgname

        main_instructions = f"You are playing 'Guess The {self.imgname}'\nThe Quiz Questions are Filtered by '{self.filter1}' {self.filter2}\nRound {self.rounds_played} Of {self.rounds_wanted}"

        # Round Lists
        self.round_aircraft = []
        self.all_answers = []
        self.full_answers = []

        # Create the window and set it to the right size
        self.play_box = Toplevel()
        self.play_box.geometry("500x720")
        self.play_box.resizable(False, False)

        # Make it so the windows close button actually closes the quiz
        self.play_box.protocol('WM_DELETE_WINDOW', root.destroy)

        # Setup required for Background
        bg_path = "C:/Users/scrap/OneDrive - Massey High School/Year 13 (2025)/TCCOUE/Aircraft Quiz/Documentation/clouds_background.jpg"  # Use correct relative path
        bg_img = Image.open(bg_path)
        resize_img = bg_img.resize((500, 720), Image.Resampling.LANCZOS)  # Resize to fit window
        bg_img = ImageTk.PhotoImage(resize_img)

        # Label Containing the Background
        play_bg = Label(self.play_box, image=bg_img)
        play_bg.place(x=0, y=0, relwidth=1, relheight=1)
        play_bg.image = bg_img

        # Main GUI Parts
        # Main Heading Title of Window
        self.start_heading = Label(self.play_box, text="Welcome To\nThe Best Aircraft Quiz",
                                   font=big_font, width=22, border=1, relief="solid")
        self.start_heading.place(x=105, y=20)
        
        # Main Quiz Instructions
        self.start_instruct = Label(self.play_box, text=main_instructions,
                                   font=small_fontb, width=50, height=3, border=1, relief="solid")
        self.start_instruct.place(x=50, y=95)

        # List for holding name button details (Text | Button # | x-Coord | y-Coord)
        play_button_list_name = [
            ["Name 1", 0, 30, 435],
            ["Name 2", 1, 275, 435],
            ["Name 3", 2, 30, 510],
            ["Name 4", 3, 275, 510]
        ]

        # List for holding image button details (Text | Button # | x-Coord | y-Coord)
        play_button_list_image = [
            ["Image 1", 0, 25, 235],
            ["Image 2", 1, 265, 235],
            ["Image 3", 2, 25, 410],
            ["Image 4", 3, 265, 410]
        ]

        # List to hold labels once they have been made
        self.buttons_ref_list = []

        # Place GUI depending on the chosen quiz mode (Guessing Images or Names)
        if imgname == "Name":
            for item in play_button_list_name:
                self.make_answer_but = Button(self.play_box, text=item[0], command=partial(self.round_results, item[1]), width=22, height=2, 
                                            font=med_font, bg="#aaaacc", border=1, relief="solid", wraplength=200, disabledforeground="#000000")
                self.make_answer_but.place(x=item[2], y=item[3])
                self.buttons_ref_list.append(self.make_answer_but)
        else:
            for item in play_button_list_image:
                self.make_answer_but = Button(self.play_box, text=item[0], command=partial(self.round_results, item[1]), bg="#000000")
                self.make_answer_but.place(x=item[2], y=item[3])
                self.buttons_ref_list.append(self.make_answer_but)

        # Quiz Instructions
        if imgname == "Name":
            self.mode_instructions = Label(self.play_box, text="Select the Name Below that\nCorresponds to the Image Above",
                                          font=small_fontb, width=30, height=2, border=1, relief="solid")            
            self.mode_instructions.place(x=130, y=375)
            self.answer_img_label = Label(self.play_box, text="Answer Image Here", border=1, relief="solid")
            self.answer_img_label.place(x=125, y=170)
        else:
            self.mode_instructions = Label(self.play_box, text=f"Select the Image Below", font=small_fontb,
                                          width=35, height=2, border=1, relief="solid")
            self.mode_instructions.place(x=110, y=165)

        # Label Telling User whether their answer was right or wrong
        self.answer_label = Label(self.play_box, text="Select the answer you think is\ncorrect and find out if you are.", font=small_font,
                            width=40, height=4, border=1, relief="solid", bg="#FFFFFF", wraplength=320)
        self.answer_label.place(x=90, y=580)

        # Trio of buttons at the bottom
        self.end_button = Button(self.play_box, text="End Game", command=self.close_play,
                                  font=med_fontb, width=15, border=1, relief="solid")
        self.end_button.place(x=40, y=670)

        self.stats_button = Button(self.play_box, text="Stats", command=self.to_stats,
                                   font=med_fontb, width=7, border=1, relief="solid")
        self.stats_button.place(x=210, y=670)
        self.stats_button.config(state=DISABLED)

        self.next_button = Button(self.play_box, text="Next Round", command=self.next_round,
                                     font=med_fontb, width=15, border=1, relief="solid")
        self.next_button.place(x=300, y=670)

        # Once interface has been created, invoke new round function for first round
        self.next_round()

    def next_round(self):
        """
        Chooses four aircraft, that have not already been picked or been answers before.
        Displays either the image or name on each button and randomly picks one aircraft to be the answer.
        """

        # Reset All Relevent Lists at the start of each round
        self.round_aircraft = []
        file_paths = []
        aircraft_names = []

        # Disable Next Round Button Until Answer Has Been Selected
        self.next_button.configure(state=DISABLED)
        # Enable All Answer Buttons
        for item in self.buttons_ref_list:
            item.configure(state=NORMAL)

        # Set Labels
        self.start_instruct.configure(text=f"You are playing 'Guess The {self.imgname}'\nThe Quiz Questions are Filtered by '{self.filter1}' {self.filter2}\nRound {self.rounds_played + 1} Of {self.rounds_wanted}")
        self.answer_label.configure(text="Select the answer you think is\ncorrect and find out if you are.", bg="#FFFFFF")

        # Get a list of all avaliable aircraft
        available_aircraft = [a for a in self.filtered_aircraft if a not in self.all_answers]

        # If we have run out of possible aircraft warn the user
        if len(available_aircraft) < 4:
            self.error_popup()
            self.all_answers = []

        # Loop until we have four different aircraft
        while len(self.round_aircraft) < 4:
            potential_aircraft = random.choice(self.filtered_aircraft)

            # Get the score and check it's not a duplicate and not already been chosen as an answer.
            if potential_aircraft not in self.round_aircraft and potential_aircraft not in self.all_answers:
                self.round_aircraft.append(potential_aircraft)

        # Aircraft Info Stuff
        main_path = "Aircraft Quiz/Aircraft Data/"

        # Get aircraft information from list
        for count, item in enumerate(self.round_aircraft):
            file = self.round_aircraft[count][3] 
            filepath = f"{main_path}{file}.jpg"
            file_paths.append(filepath)
            aircraft_names.append(self.round_aircraft[count][0])

        # Pick one of the 4 aircraft to be the correct answer
        ans_num = random.randint(0, 3)

        # Get the image name and aircraft name of the answer
        ans_img = file_paths[ans_num]
        ans_name = aircraft_names[ans_num]
        self.ans_name = ans_name

        # Add all answers to a list so we dont get them again
        self.all_answers.append(self.round_aircraft[ans_num])
        self.full_answers.append(self.round_aircraft[ans_num])
        # If user plays Guess the Image
        if self.imgname == "Image": 
            # Answer to choose label
            self.mode_instructions.configure(text=f"Select the Image Below that is a\n{ans_name}")

            # 4 Image display
            img1 = ImageTk.PhotoImage(Image.open(file_paths[0]).resize((200, 144)))
            img2 = ImageTk.PhotoImage(Image.open(file_paths[1]).resize((200, 144)))
            img3 = ImageTk.PhotoImage(Image.open(file_paths[2]).resize((200, 144)))
            img4 = ImageTk.PhotoImage(Image.open(file_paths[3]).resize((200, 144)))
            name1 = aircraft_names[0]
            name2 = aircraft_names[1]
            name3 = aircraft_names[2]
            name4 = aircraft_names[3]

            button1 = self.buttons_ref_list[0]
            button1.configure(text=name1, image=img1, bg="#000000")
            button1.image = img1

            button2 = self.buttons_ref_list[1]
            button2.configure(text=name2, image=img2, bg="#000000")
            button2.image = img2

            button3 = self.buttons_ref_list[2]
            button3.configure(text=name3, image=img3, bg="#000000")
            button3.image = img3

            button4 = self.buttons_ref_list[3]
            button4.configure(text=name4, image=img4, bg="#000000")
            button4.image = img4

        # If users plays guess the name
        else:
            # Display Image for correct answer
            answer_image = ImageTk.PhotoImage(Image.open(ans_img).resize((250, 180)))
            self.answer_img_label.configure(image=answer_image)
            self.answer_img_label.image = answer_image

            # 4 Name Display
            name1 = aircraft_names[0]
            name2 = aircraft_names[1]
            name3 = aircraft_names[2]
            name4 = aircraft_names[3]

            button1 = self.buttons_ref_list[0]
            button1.configure(text=name1, bg="#FFFFFF")

            button2 = self.buttons_ref_list[1]
            button2.configure(text=name2, bg="#FFFFFF")

            button3 = self.buttons_ref_list[2]
            button3.configure(text=name3, bg="#FFFFFF")

            button4 = self.buttons_ref_list[3]
            button4.configure(text=name4, bg="#FFFFFF")

    def round_results(self, button_pressed):
        """
            Retrieves which button was pushed (index 0 - 3), retrives
            score and then compares it with median, updates results
            and adds results to stats list.
        """
        # Enable Next Round & Stats Button
        self.next_button.configure(state=NORMAL)
        self.stats_button.configure(state=NORMAL)

        # Disable All Answer Buttons
        for count, button in enumerate(self.buttons_ref_list):
            button.configure(state=DISABLED)
            button_name = self.buttons_ref_list[count].cget('text')
            if button_name == self.ans_name:
                self.buttons_ref_list[count].configure(bg="#55FF55")
            else:
                self.buttons_ref_list[count].configure(bg="#FF5050")

        # Update Rounds Played
        self.rounds_played += 1

        # Determine whether user got correct answer
        user_button_name = self.buttons_ref_list[button_pressed].cget('text')
        if user_button_name == self.ans_name:
            # If user answer is correct
            self.answer_label.configure(text=f"The {user_button_name}\nis the Correct Answer!!!\nCongratulations.", bg="#55FF55")
            self.rounds_won += 1
        else:
            # If user answer is wrong
            self.answer_label.configure(text=f"The {user_button_name} is NOT the Correct Answer... The Correct Answer is The {self.ans_name}.\nGood Luck Next Time!", bg="#FF5050")

        # End of Quiz
        if self.rounds_played == self.rounds_wanted:
            self.next_button.configure(state=DISABLED, text="Game Over")
            self.end_button.configure(text="Play Again")

    def close_play(self):
        """
        Closes the whole play window and reshows the main, start game window
        """
        # Reshow root (Start Game window) and end current game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_stats(self):
        """
        Retrieves everything we need to display the game / round stats
        """
        # Transport all the required information across the classes
        stats_bundle = [self.rounds_won, self.rounds_played, self.rounds_wanted, self.full_answers]

        # Disables trio of bottom buttons so user doesn't break the game clicking them
        self.end_button.configure(state=DISABLED)
        self.stats_button.configure(state=DISABLED)

        DisplayStats(self, stats_bundle)

    def end_here(self):
        """
        Used by the error popup, closes shows main, start game window, and closes error popup and play window
        """
        root.deiconify()
        self.play_box.destroy()
        self.error_box.destroy()

    def continue_here(self):
        """
        Used by error popup, closes error popup and re-enables all the buttons so user can continue playing.
        """
        # Get rid of error popup window
        self.error_box.destroy()
        # Re-Enable play_box buttons
        self.next_button.configure(state=NORMAL)
        self.stats_button.configure(state=NORMAL)
        self.end_button.configure(state=NORMAL)
        # Re-Enable answer buttons
        for button in self.buttons_ref_list:
            button.configure(state=NORMAL)

    def error_popup(self):
        """
        Makes a new window that asks the user if they want to continue or end here
        when the game runs out of new aircraft.
        """
        # Make the window for error popup
        self.error_box = Toplevel()
        self.error_box.resizable(False, False)
        # Make a frame to put all widgets in
        error_frame = Frame(self.error_box, bg="#608DAA")
        error_frame.grid()

        # Disable play_box buttons
        self.next_button.configure(state=DISABLED)
        self.stats_button.configure(state=DISABLED)
        self.end_button.configure(state=DISABLED)
        # Disable answer buttons
        for button in self.buttons_ref_list:
            button.configure(state=DISABLED)

        # Long string for error
        error = "The amount of rounds you chose along with the filters you chose means\n" \
                "that you have already gone through all the different questions/answers\n" \
                "there are for these settings.\n\n" \
                "You now have the choice of continuing with the possibility of repeated\n" \
                "questions/answers, or ending here and returning to the start menu."

        # GUI for popup
        error_heading = Label(error_frame, text="We Have Run Out of Aircraft!!!", font=med_fontb, border=1, relief="solid", padx=5, pady=5)
        error_heading.grid(row=0, pady=10)

        error_label = Label(error_frame, text=error, font=small_font, border=1, relief="solid", padx=5, pady=5)
        error_label.grid(row=1, padx=10)

        buttons_frame = Frame(error_frame, bg="#608DAA")
        buttons_frame.grid(row=2, pady=10)

        end_button = Button(buttons_frame, text="End Quiz Here", font=med_fontb, command=self.end_here, width=15)
        end_button.grid(row=0, column=0, padx=5)

        continue_button = Button(buttons_frame, text="Continue Playing", font=med_fontb, command=self.continue_here, width=15)
        continue_button.grid(row=0, column=1, padx=5)


class DisplayInstructions():

    def __init__(self, partner):
        # Long String of instructions
        full_instructions = "Before you start the quiz, you should select the filters that you want.\n\n" \
                            "First, whether you want to be quizzed on the Images or the Names.\n" \
                            "When quizzed on Images you are given a name and choose from 4 images.\n" \
                            "When quizzed on Names you are given an image and choose from 4 names.\n\n" \
                            "You can also filter by:\n" \
                            "Only Planes, Only Helicopters or Both &\n" \
                            "Only Civilian Aircraft, Only Military Aircraft or Both\n\n" \
                            "Once you choose your filters, you enter how many rounds (Questions)\n" \
                            "you want to be quizzed on and click 'Play Quiz'\n" \
                            "You can only play between 0 and 1000 rounds\n" \
                            "(Not that there is more than 150 different aircraft)\n\n" \
                            "If you choose the play more than for example 12 rounds of\n" \
                            "'Civilian Helicopters' there you will run out of aircraft in round 9\n" \
                            "You can then choose to continue with repeated question or just end there."
        
        # Makes new window seperate to main converter window
        self.instructions_box = Toplevel()

        # Disable hints button when already open
        partner.start_instruct.config(state=DISABLED)

        # If users press cross at top, closes hints and 'releases' hints button
        self.instructions_box.protocol('WM_DELETE_WINDOW', partial(self.close_instructions, partner))

        self.instructions_frame = Frame(self.instructions_box)
        self.instructions_frame.grid()

        self.instructions_heading = Label(self.instructions_frame, text="Full Instructions", font=med_fontb)
        self.instructions_heading.grid(row=0)

        self.instructions_text = Label(self.instructions_frame, text=full_instructions, font=small_font, justify="left")
        self.instructions_text.grid(row=1, padx=10)

        self.dismiss_button = Button(self.instructions_frame, font=med_fontb,
                                     text="Dismiss", command=partial(self.close_instructions, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10) 

    def close_instructions(self, partner):
        """
        Closes instructions dialogue box (and enables instructions button)
        """
        # Allows instructions, end and start game button to be used again
        partner.start_instruct.config(state=NORMAL)
        partner.end_game_but.config(state=NORMAL)
        partner.start_game_but.config(state=NORMAL)

        self.instructions_box.destroy()


class DisplayStats():
    """
    Display stats window for the Aircraft Quiz
    """

    def __init__(self, partner, all_stats_info):
        # Detect State of Quiz
        self.next_state = partner.next_button.cget("state")
        if self.next_state == "normal":
            # Disable next round button
            partner.next_button.configure(state=DISABLED)
        else:
            # Disable answer buttons
            for button in partner.buttons_ref_list:
                button.configure(state=DISABLED)

        # Extract information from the master list...
        rounds_won = all_stats_info[0]
        rounds_played = all_stats_info[1]
        rounds_wanted = all_stats_info[2]
        full_answers = all_stats_info[3]

        # Make new window for stats
        self.stats_box = Toplevel()
        self.stats_box.resizable(False, False)

        # If users press cross at top, closes stats and 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        # Frame for all widgets to go in
        self.stats_frame = Frame(self.stats_box, bg="#608DAA")
        self.stats_frame.grid()

        # Maths for Stats
        success_rate = rounds_won / rounds_played * 100

        # All label Strings
        success_string = f"Success Rate: {rounds_won} / {rounds_played} ({success_rate:.2f}%)"

        rounds_string = f"You have played {rounds_played} out of the {rounds_wanted} rounds entered.\n" \
                        f"You have won {rounds_won} of these rounds."
        
        # Comment String
        if rounds_won == rounds_played:
            comment_string = "CONGRATS! You guessed every aircraft correctly.\nNot many poeple can do that..."
        
        elif rounds_won == 0:
            comment_string = "OH NO! You didn't get any aircraft correct...\nRemind me to never let you fly me anywhere."

        else:
            comment_string = "You are doing well.\nKeeping trying, you will get them all eventually."


        # Label List (text | font | 'Sticky')
        all_stats_strings = [
            ["Statistics", big_font],
            [success_string, med_font],
            [comment_string, med_font],
            [rounds_string, med_font],
        ]

        # List to hold labels once they have been made
        stats_labels_ref_list = []

        # Loop through every item in label list to make label
        for count, item in enumerate(all_stats_strings):
            self.make_stats_label = Label(self.stats_frame, text=item[0], font=item[1], bg="#608DAA")
            self.make_stats_label.grid(row=count, pady=5)
            stats_labels_ref_list.append(self.make_stats_label)

        self.dismiss_button = Button(self.stats_frame, font=med_fontb, text="Close", command=partial(self.close_stats, partner), width=10)
        self.dismiss_button.grid(row=4, padx=10)

    def close_stats(self, partner):
        """
        Closes stats dialogue box (and enables stats button)
        """
        # Allows hints, stats and end game button to be used again
        partner.end_button.config(state=NORMAL)
        partner.stats_button.config(state=NORMAL)

        if self.next_state == "normal":
            # Disable next round button
            partner.next_button.configure(state=NORMAL)
        else:
            # Disable answer buttons
            for button in partner.buttons_ref_list:
                button.configure(state=NORMAL)

        self.stats_box.destroy()


# Main Routine
if __name__ == "__main__":
    root = Tk()
    root.title("The Best Aircraft Quiz")
    root.geometry("500x720")
    root.resizable(False, False)
    StartGame()
    root.mainloop()