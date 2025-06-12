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
                self.filter_aircraft(self.imgname_filt, self.planeheli_filt, self.civmil_filt)
                Play(rounds_wanted, self.imgname_filter, self.ph_filt, self.cm_filt)
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

        # Reset Option Buttons
        self.imgname_filt.set(0)
        self.planeheli_filt.set(0)
        self.civmil_filt.set(0)

        return filtered_aircraft


class Play():
    """
    Interface for playing the Aircraft Quiz
    """

    def __init__(self, how_many, imgname, filt1, filt2):

        # Set filters for better looks
        if filt1 == "Both" and filt2 == "Both":
            filter1 = "EVERYTHING"
            filter2 = ""
        else:
            filter1 = filt1
            filter2 = f"& '{filt2}'"

        # Set strings
        round_num = 0
        main_instructions = f"You are playing 'Guess The {imgname}'\nThe Questions are Filtered by '{filter1}' {filter2}\nRound {round_num} Of {how_many}"
        
        # TEMP AIRCRAFT NAME
        self.answer_name = "*Name Of Answer Aircraft*"

        # TEMP IMAGE PATHS
        # Image location (add "/" not "\")
        i1 = Image.open("C:/Users/scrap/OneDrive - Massey High School/Year 13 (2025)/TCCOUE/Aircraft Quiz/Aircraft Data/Sikorsky-UH-60 Black-Hawk.jpg")
        i2 = Image.open("C:/Users/scrap/OneDrive - Massey High School/Year 13 (2025)/TCCOUE/Aircraft Quiz/Aircraft Data/Boeing-747-8.jpg")
        i3 = Image.open("C:/Users/scrap/OneDrive - Massey High School/Year 13 (2025)/TCCOUE/Aircraft Quiz/Aircraft Data/Sukhoi Su-25.jpg")
        i4 = Image.open("C:/Users/scrap/OneDrive - Massey High School/Year 13 (2025)/TCCOUE/Aircraft Quiz/Aircraft Data/F7U Cutlass.jpg")
        answer_i = Image.open("C:/Users/scrap/OneDrive - Massey High School/Year 13 (2025)/TCCOUE/Aircraft Quiz/Aircraft Data/U-2 Dragon Lady.jpg")
        i1 = i1.resize((200, 144))
        i2 = i2.resize((200, 144))
        i3 = i3.resize((200, 144))
        i4 = i4.resize((200, 144))
        answer_i = answer_i.resize((250, 180))
        img1 = ImageTk.PhotoImage(i1)
        img2 = ImageTk.PhotoImage(i2)
        img3 = ImageTk.PhotoImage(i3)
        img4 = ImageTk.PhotoImage(i4)
        answer_img = ImageTk.PhotoImage(answer_i)

        # Setup radiobutton variable
        self.answer_select = StringVar()

        # Create the window and set it to the right size
        self.play_box = Toplevel()
        self.play_box.geometry("500x720")
        self.play_box.resizable(False, False)

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

        # List for holding name radiobutton details (Text | Variable | Value | x-Coord | y-Coord)
        play_radio_list_name = [
            ["Name 1", self.answer_select, 0, 30, 435],
            ["Name 2", self.answer_select, 1, 265, 435],
            ["Name 3", self.answer_select, 2, 30, 510],
            ["Name 4", self.answer_select, 3, 265, 510]
        ]

        # List for holding image radiobutton details (Text | ImageName | Variable | Value | x-Coord | y-Coord | Width | Height)
        play_radio_list_image = [
            [img1, self.answer_select, 0, 25, 235],
            [img2, self.answer_select, 1, 265, 235],
            [img3, self.answer_select, 2, 25, 420],
            [img4, self.answer_select, 3, 265, 420]
        ]

        # List to hold labels once they have been made
        self.answers_ref_list = []

        # Place GUI depending on the chosen quiz mode (Guessing Images or Names)
        if imgname == "Name":
            for item in play_radio_list_name:
                self.make_answer_but = Radiobutton(self.play_box, text=item[0], variable=item[1], value=item[2], width=22, height=2, 
                                            font=med_font, bg="#aaaacc", selectcolor="#dddddd", border=1, relief="solid", indicatoron=0)
                self.make_answer_but.place(x=item[3], y=item[4])
                self.answers_ref_list.append(self.make_answer_but)
        else:
            for item in play_radio_list_image:
                self.make_answer_but = Radiobutton(self.play_box, image=item[0], variable=item[1], value=item[2],
                                            bg="#000000", indicatoron=0)
                self.make_answer_but.place(x=item[3], y=item[4])
                self.make_answer_but.image = item[0]
                self.answers_ref_list.append(self.make_answer_but)

        # Quiz Instructions
        if imgname == "Name":
            self.mode_instructions = Label(self.play_box, text="Select the Name Below that\nCorresponds to the Image Above",
                                           font=small_fontb, width=30, border=1, relief="solid")            
            self.mode_instructions.place(x=130, y=375)
            self.answer_img_label = Label(self.play_box, image=answer_img, bg="#000000")
            self.answer_img_label.place(x=125, y=170)
            self.answer_img_label.image = answer_img
        else:
            self.mode_instructions = Label(self.play_box, text=f"Select the Image Below that is a\n{self.answer_name}",
                                           font=small_fontb, width=35, height=2, border=1, relief="solid")
            self.mode_instructions.place(x=110, y=165)

        # Trio of buttons at the bottom
        self.return_menu = Button(self.play_box, text="Return To Menu", command=self.close_play,
                                  font=med_fontb, width=15, border=1, relief="solid")
        self.return_menu.place(x=40, y=650)

        self.stats_button = Button(self.play_box, text="Stats", command=self.to_stats,
                                   font=med_fontb, width=7, border=1, relief="solid")
        self.stats_button.place(x=210, y=650)
        self.stats_button.config(state=DISABLED)

        self.round_button = Button(self.play_box, text="Next Round", command=self.next_round,
                                     font=med_fontb, width=15, border=1, relief="solid")
        self.round_button.place(x=300, y=650)

    def close_play(self):
        # Reshow root (Start Game window) and end current game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_stats(self):
        pass

    def next_round(self):
        pass


# Main Routine
if __name__ == "__main__":
    root = Tk()
    root.title("The Best Aircraft Quiz")
    root.geometry("500x720")
    root.resizable(False, False)
    StartGame()
    root.mainloop()