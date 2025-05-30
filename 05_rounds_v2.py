from tkinter import *
from PIL import ImageTk, Image
import csv
import random
from functools import partial

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


class StartGame():
    def __init__(self):
        # SET FILTERS AND ROUNDS HERE
        self.imgname_filt = "0"
        self.planeheli_filt = "1"
        self.civmil_filt = "2"
        rounds = 2

        self.check_rounds(rounds)
        
    def check_rounds(self, rounds):
        """
        Checks whether users input for rounds is valid
        """
        # Retrieve temperature to be converted
        rounds_wanted = rounds

        has_errors = "no"

        # Checks that amount to be converted is a number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Invoke Play Class (and take across number of rounds)
                aircraft_list = self.filter_aircraft(self.imgname_filt, self.planeheli_filt, self.civmil_filt)
                Play(rounds_wanted, self.imgname_filter, self.ph_filt, self.cm_filt, aircraft_list)
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

        return filtered_aircraft


class Play():
    """
    Interface for playing the Aircraft Quiz
    """

    def __init__(self, how_many, imgname, filt1, filt2, filtered_aircraft):
        # Game Variables
        self.rounds_played = 0

        self.rounds_wanted = how_many

        self.rounds_won = 0

        self.filtered_aircraft = filtered_aircraft

        self.imgname = imgname

        # Round Lists
        self.round_aircraft = []

        # Main GUI Parts
        # Display Rounds in Widget
        self.rounds_label = Label(root, text=f"Round 0 of {how_many}", font=small_fontb)
        self.rounds_label.grid(row=0)

        # Frame to hold buttons depending on what mode user chooses
        self.button_frame = Frame(root)
        self.button_frame.grid(row=3)

        # List for holding name button details (Text | Button # | x-Coord | y-Coord)
        # play_button_list_name = [
        #     ["Name 1", 0, 30, 435],
        #     ["Name 2", 1, 275, 435],
        #     ["Name 3", 2, 30, 525],
        #     ["Name 4", 3, 275, 525]
        # ]
        play_button_list_name = [
            ["Name 1", 0, 0, 0],
            ["Name 2", 1, 0, 1],
            ["Name 3", 2, 1, 0],
            ["Name 4", 3, 1, 1]
        ]

        # List for holding image button details (Text | Button # | x-Coord | y-Coord)
        # play_button_list_image = [
        #     ["Image 1", 0, 25, 235],
        #     ["Image 2", 1, 265, 235],
        #     ["Image 3", 2, 25, 420],
        #     ["Image 4", 3, 265, 420]
        # ]
        play_button_list_image = [
            ["Image 1", 0, 0, 0],
            ["Image 2", 1, 0, 1],
            ["Image 3", 2, 1, 0],
            ["Image 4", 3, 1, 1]
        ]

        # List to hold buttons once they have been made
        self.buttons_ref_list = []

        # Place GUI depending on the chosen quiz mode (Guessing Images or Names)
        if imgname == "Name":
            for item in play_button_list_name:
                self.make_answer_but = Button(self.button_frame, text=item[0], command=partial(self.round_results, "Name", item[1]), width=22, height=2, 
                                            font=med_font, bg="#aaaacc", border=1, relief="solid")
                self.make_answer_but.grid(row=item[2], column=item[3])
                self.buttons_ref_list.append(self.make_answer_but)
        else:
            for item in play_button_list_image:
                self.make_answer_but = Button(self.button_frame, text=item[0], command=partial(self.round_results, "Image", item[1]), bg="#000000")
                self.make_answer_but.grid(row=item[2], column=item[3])
                self.buttons_ref_list.append(self.make_answer_but)

        # Display extra buttons depending on mode selected
        if imgname == "Name":
            # Display Image for correct answer
            self.image_label = Label(root, text="Answer Image Here", border=1, relief="solid")
            self.image_label.grid(row=1, pady=5)
            # Small instructions label
            self.instructions_label = Label(root, text="Select the Name Below that\nCorresponds to the Image Above", font=small_fontb, width=30, height=2,
                            border=1, relief="solid")
            self.instructions_label.grid(row=2, pady=5)
            
        else:
            # Name of Aircraft to choose - label
            self.name_label = Label(root, text=f"Select the Image Below", font=med_fontb, width=35)
            self.name_label.grid(row=1)

        self.answer_label = Label(root, text="Select the answer you think is\ncorrect and find out if you are.", font=small_font,
                            border=1, relief="solid", bg="#FFFFFF")
        self.answer_label.grid(row=4, pady=5)

        end_frame = Frame(root)
        end_frame.grid(row=5)

        self.end_button = Button(end_frame, text="End Game", font=med_fontb, command=self.close_play,
                                border=1, relief="solid")
        self.end_button.grid(row=0, column=0)

        self.next_button = Button(end_frame, text="Next Round", font=med_fontb, command=self.next_round,
                                border=1, relief="solid")
        self.next_button.grid(row=0, column=1)

        # Once interface has been created, invoke new round function for first round
        self.next_round()

    def next_round(self):
        # Reset All Relevent Lists at the start of each round
        self.round_aircraft = []
        file_paths = []
        aircraft_names = []

        # Disable Next Round Button Until Answer Has Been Selected
        self.next_button.configure(state=DISABLED)

        # Set Rounds Label
        self.rounds_label.configure(text=f"Round {self.rounds_played + 1} of {self.rounds_wanted}")

        # Loop until we have four different aircraft,
        while len(self.round_aircraft) < 4:
            potential_aircraft = random.choice(self.filtered_aircraft)

            # Get the score and check it's not a duplicate
            if potential_aircraft not in self.round_aircraft:
                self.round_aircraft.append(potential_aircraft)

        print("Round Aircraft: ", self.round_aircraft)
        print()

        # Aircraft Info Stuff
        main_path = "Aircraft Quiz/Aircraft Data/"

        # Get aircraft information from list
        for count, item in enumerate(self.round_aircraft):
            file = self.round_aircraft[count][3] 
            filepath = f"{main_path}{file}.jpg"
            file_paths.append(filepath)
            aircraft_names.append(self.round_aircraft[count][0])

        print("File Paths: ", file_paths)
        print()
        print("Aircraft Names: ", aircraft_names)

        # Pick one of the 4 aircraft to be the correct answer
        ans_num = random.randint(0, 3)

        # Get the image name and aircraft name of the answer
        ans_img = file_paths[ans_num]
        ans_name = aircraft_names[ans_num]

        print("Answer Image Path: ", ans_img)
        print("Answer Aircraft Name: ", ans_name)

        # If user plays Guess the Image
        if self.imgname == "Image": 
            # Answer to choose label
            self.name_label.configure(text=f"Select the Image Below that is a\n{ans_name}")

            # 4 Image display
            img1 = ImageTk.PhotoImage(Image.open(file_paths[0]).resize((200, 144)))
            img2 = ImageTk.PhotoImage(Image.open(file_paths[1]).resize((200, 144)))
            img3 = ImageTk.PhotoImage(Image.open(file_paths[2]).resize((200, 144)))
            img4 = ImageTk.PhotoImage(Image.open(file_paths[3]).resize((200, 144)))

            button1 = self.buttons_ref_list[0]
            button1.configure(image=img1)
            button1.image = img1

            button2 = self.buttons_ref_list[1]
            button2.configure(image=img2)
            button2.image = img2

            button3 = self.buttons_ref_list[2]
            button3.configure(image=img3)
            button3.image = img3

            button4 = self.buttons_ref_list[3]
            button4.configure(image=img4)
            button4.image = img4

        # If users plays guess the name
        else:
            # Display Image for correct answer
            answer_image = ImageTk.PhotoImage(Image.open(ans_img).resize((250, 180)))
            self.image_label.configure(image=answer_image)
            self.image_label.image = answer_image

            # 4 Name Display
            name1 = aircraft_names[0]
            name2 = aircraft_names[1]
            name3 = aircraft_names[2]
            name4 = aircraft_names[3]

            button1 = self.buttons_ref_list[0]
            button1.configure(text=name1)

            button2 = self.buttons_ref_list[1]
            button2.configure(text=name2)

            button3 = self.buttons_ref_list[2]
            button3.configure(text=name3)

            button4 = self.buttons_ref_list[3]
            button4.configure(text=name4)

    def round_results(self, button_type, button_pressed):
        """
            Retrieves which button was pushed (index 0 - 3), retrives
            score and then compares it with median, updates results
            and adds results to stats list.
        """
        print(f"The {button_type} Button Pressed Was #{button_pressed}" )

        # Enable Next Round Button
        self.next_button.configure(state=NORMAL)

        # Update Rounds Played
        self.rounds_played += 1

        # End of Quiz
        if self.rounds_played == self.rounds_wanted:
            self.next_button.configure(state=DISABLED, text="Game Over", bg="#FF5050")
            self.end_button.configure(text="Play Again", bg="#00FF55")

    def close_play(self):
        root.destroy()


# Main Routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
