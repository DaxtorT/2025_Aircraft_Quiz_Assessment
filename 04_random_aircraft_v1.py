from tkinter import *
from PIL import ImageTk, Image
import csv
import random

root = Tk()

# Global Variables
big_font = ("B612", "16", "bold")
med_font = ("B612", "12")
med_fontb = ("B612", "12", "bold")
small_font = ("B612", "10")
small_fontb = ("B612", "10", "bold")

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

def check_rounds(self, rounds):
    """
    Checks whether users input for rounds is valid
    """
    # Retrieve temperature to be converted
    rounds_wanted = rounds.get()

    has_errors = "no"

    # Checks that amount to be converted is a number above absolute zero
    try:
        rounds_wanted = int(rounds_wanted)
        if rounds_wanted > 0:
            # Invoke Play Class (and take across number of rounds)
            filter_aircraft(self.imgname_filt, self.planeheli_filt, self.civmil_filt)
            Play(rounds_wanted, self.imgname_filter, self.ph_filt, self.cm_filt)
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
    ph_filt = filt1
    if ph_filt == "1":
        self.ph_filt = "Plane"
    elif ph_filt == "2":
        self.ph_filt = "Helicopter"
    else:
        self.ph_filt = "Both"
    cm_filt = filt2
    if cm_filt == "1":
        self.cm_filt = "Civilian"
    elif cm_filt == "2":
        self.cm_filt = "Military"
    else:
        self.cm_filt = "Both"

    imgname_filt = imgname
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

    # Set list to 'global'
    self.filtered_aircraft = filtered_aircraft

    return filtered_aircraft

# SET FILTERS AND ROUNDS HERE
image_name = "0"
civilian_military = "2"
plane_helicopter = "1"
rounds = 2

filtered_list = filter_aircraft(root, image_name, plane_helicopter, civilian_military)

class Play:
    """
    Interface for playing the Colour Quest Game
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
            ["Name 2", self.answer_select, 1, 275, 435],
            ["Name 3", self.answer_select, 2, 30, 525],
            ["Name 4", self.answer_select, 3, 275, 525]
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

round_aircraft = []
 
# Loop until we have four aircraft with different scores,
while len(round_aircraft) < 4:
    potential_aircraft = random.choice(filtered_list)

    # Get the score and check it's not a duplicate
    if potential_aircraft[0] not in round_aircraft:
        round_aircraft.append(potential_aircraft)

print("Round Aircraft: ", round_aircraft)
print()

# Image Paths Stuff
main_path = "C:/Users/scrap/OneDrive - Massey High School/Year 13 (2025)/TCCOUE/Aircraft Quiz/Aircraft Data/"
file_paths = []

# Get image file names from list
for count, item in enumerate(round_aircraft):
    file = round_aircraft[count][3]
    filepath = f"{main_path}{file}.jpg"
    file_paths.append(filepath)

print("File Paths: ", file_paths)
print()

i1 = Image.open(file_paths[0]).resize((200, 144))
i2 = Image.open(file_paths[1]).resize((200, 144))
i3 = Image.open(file_paths[2]).resize((200, 144))
i4 = Image.open(file_paths[3]).resize((200, 144))
img1 = ImageTk.PhotoImage(i1)
img2 = ImageTk.PhotoImage(i2)
img3 = ImageTk.PhotoImage(i3)
img4 = ImageTk.PhotoImage(i4)


image1 = Label(root, image=img1)
image1.grid(row=0, column=0)

image2 = Label(root, image=img2)
image2.grid(row=0, column=1)

image3 = Label(root, image=img3)
image3.grid(row=1, column=0)

image4 = Label(root, image=img4)
image4.grid(row=1, column=1)

mainloop()
