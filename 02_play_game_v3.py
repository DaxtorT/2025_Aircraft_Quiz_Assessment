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

        # Setup for radiobuttons
        self.imgname_filt = StringVar()
        self.planeheli_filt = StringVar()
        self.civmil_filt = StringVar()

        # Main Heading Title of Window
        self.start_heading = Label(root, text="Welcome To\nThe Best Aircraft Quiz",
                                   font=("B612", "16", "bold"), width=22, border=1, relief="solid")
        self.start_heading.place(x=105, y=20)

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

        has_errors = "no"

        # Checks that amount to be converted is a number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Invoke Play Class (and take across number of rounds)
                aircraft_list = self.filter_aircraft(self.imgname_filt, self.planeheli_filt, self.civmil_filt)
                Play(rounds_wanted, self.imgname_filter, self.ph_filt, self.cm_filt, aircraft_list)
                # Reset Start Game Window for if user returns
                self.round_entry.delete(0, END)

                # Hide Root Window (ie: hide rounds choice window)
                root.withdraw()
            else:
                has_errors == "yes"

        except ValueError:
            has_errors = "yes"

        # Display the error if necessary
        if has_errors == "yes":
            # Re-enable start game button if error occurs
            self.start_game_but.config(state=NORMAL)
            # Change label and entry box to show error
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


class Play():
    """
    Interface for playing the Aircraft Quiz
    """

    def __init__(self, how_many, imgname, filt1, filt2, filtered_aircraft):
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
                self.make_answer_but = Button(self.play_box, text=item[0], command=partial(self.round_results, "Name", item[1]), width=22, height=2, 
                                            font=med_font, bg="#aaaacc", border=1, relief="solid", wraplength=200, disabledforeground="#000000")
                self.make_answer_but.place(x=item[2], y=item[3])
                self.buttons_ref_list.append(self.make_answer_but)
        else:
            for item in play_button_list_image:
                self.make_answer_but = Button(self.play_box, text=item[0], command=partial(self.round_results, "Image", item[1]), bg="#000000")
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

    def round_results(self, button_type, button_pressed):
        """
            Retrieves which button was pushed (index 0 - 3), retrives
            score and then compares it with median, updates results
            and adds results to stats list.
        """
        # Enable Next Round Button
        self.next_button.configure(state=NORMAL)
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
        else:
            # If user answer is wrong
            self.answer_label.configure(text=f"The {user_button_name} is NOT the Correct Answer... The Correct Answer is The {self.ans_name}.\nGood Luck Next Time!", bg="#FF5050")

        # End of Quiz
        if self.rounds_played == self.rounds_wanted:
            self.next_button.configure(state=DISABLED, text="Game Over")
            self.end_button.configure(text="Play Again")

    def close_play(self):
        # Reshow root (Start Game window) and end current game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_stats(self):
        pass

    def error_popup(self):
        print("I AM A POPUP FOR ERRORS")
        # Disable play_box buttons
        self.next_button.configure(state=DISABLED)
        self.stats_button.configure(state=DISABLED)
        self.end_button.configure(state=DISABLED)
        # Disable answer buttons
        for item in self.buttons_ref_list:
            item.configure(state=DISABLED)

# Main Routine
if __name__ == "__main__":
    root = Tk()
    root.title("The Best Aircraft Quiz")
    root.geometry("500x720")
    root.resizable(False, False)
    StartGame()
    root.mainloop()