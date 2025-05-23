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

def get_names():
    """
    Get names from the csv and return a list of names
    """
    print("Get Names")


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
        self.start_heading.place(x=110, y=20)
        
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
        self.end_game_but = Button(root, text="🚫 End Quiz 🚫", command=self.end_quiz,
                                   font=("B612", "16", "bold"), width=13, border=1, relief="solid")
        self.end_game_but.place(x=30, y=650)

        self.start_game_but = Button(root, text="✅ Play Quiz ✅", command=self.check_rounds,
                                     font=("B612", "16", "bold"), width=13, border=1, relief="solid")
        self.start_game_but.place(x=295, y=650)

    def check_rounds(self):
        """
        Checks whether users input for rounds is valid
        """
        # Disable start game button
        self.start_game_but.config(state=DISABLED)

        # Retrieve temperature to be converted
        rounds_wanted = self.round_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.round_instruct.config(fg="#000000", text=self.round_instructions, font=small_fontb)
        self.round_entry.config(bg="#ffffff")

        error = "Oops - Please choose a whole number more than zero."
        has_errors = "no"

        # Checks that amount to be converted is a number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Invoke Play Class (and take across number of rounds)
                self.filter_aircraft(self.planeheli_filt, self.civmil_filt)
                Play(rounds_wanted, self.ph_filt, self.cm_filt)
                # Hide Root Window (ie: hide rounds choice window)
                #root.withdraw()
            else:
                has_errors == "yes"

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
        print("End Quiz")

    def filter_aircraft(self, filt1, filt2):
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

        # Temp print the list of aircraft
        print(f"Full List of Aircraft: {all_aircraft}\n\n")

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
                if aircraft[2] == self.ph_filt:
                    planeheli_aircraft.append(aircraft)
                
        # Civlian/Military Filter work
        for aircraft in planeheli_aircraft:
            # If filter is 'Both' just all all aircraft to list
            if self.cm_filt == "Both":
                filtered_aircraft.append(aircraft)
            # If filter isn't 'Both' then only add aircraft with corresponding type
            else:
                if aircraft[3] == self.cm_filt:
                    filtered_aircraft.append(aircraft)

        # Set list to 'global'
        self.filtered_aircraft = filtered_aircraft

        # Temp Print Filtered List
        print(f"\n\nFiltered List of Aircraft ({self.ph_filt}, {self.cm_filt}):\n{filtered_aircraft}")

        return filtered_aircraft


class DisplayInstructions():

    def __init__(self, partner):
        # Long String of instructions
        full_instructions = "Before you start the quiz, you should select the filters that you want.\n\n" \
                            "First, whether you want to be quizzed on the Images or the Names.\n" \
                            "When quizzed on Images you are given a name and choose from 4 images.\n" \
                            "When quizzed on Names you are given an image and choose from 4 names.\n\n" \
                            "You can also filter by:\n" \
                            "Only Planes, Only Helicopters or Both\n" \
                            "Only Civilian Aircraft, Only Military Aircraft or Both &\n\n" \
                            "Once you choose your filters, you enter how many rounds (Questions)\n" \
                            "you want to be quizzed on and click 'Play Quiz'"
        
        # Makes new window seperate to main converter window
        self.instructions_box = Toplevel()

        # Disable hints button when already open
        partner.start_instruct.config(state=DISABLED)

        # If users press cross at top, closes hints and 'releases' hints button
        self.instructions_box.protocol('WM_DELETE_WINDOW', partial(self.close_instructions, partner))

        self.instructions_frame = Frame(self.instructions_box, width=300, height=200)
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


class Play:
    """
    Interface for playing the Colour Quest Game
    """

    def __init__(self, how_many, filt1, filt2):
        self.play_box = Toplevel()
        self.play_box.geometry("500x720")
        self.play_box.resizable(False, False)

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.game_heading = Label(self.game_frame, text=f"Round 0 of {how_many}",
                                  font=("Arial", "16", "bold"))
        self.game_heading.grid(row=0)

        self.game_instruct = Label(self.game_frame, text=f"You are playing the Aircraft Quiz filtered by {filt2} {filt1}'s")
        self.game_instruct.grid(row=1)

# Main Routine
if __name__ == "__main__":
    root = Tk()
    root.title("The Best Aircraft Quiz")
    root.geometry("500x720")
    root.resizable(False, False)
    StartGame()
    root.mainloop()