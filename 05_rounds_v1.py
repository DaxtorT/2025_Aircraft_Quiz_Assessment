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
        # Setup
        rounds_played = 0
        round_aircraft = []
        
        # Loop until we have four aircraft with different scores,
        while len(round_aircraft) < 4:
            potential_aircraft = random.choice(filtered_aircraft)

            # Get the score and check it's not a duplicate
            if potential_aircraft not in round_aircraft:
                round_aircraft.append(potential_aircraft)

        print("Round Aircraft: ", round_aircraft)
        print()

        # Aircarft Info Stuff
        main_path = "Aircraft Quiz/Aircraft Data/"
        file_paths = []
        aircraft_names = []

        # Get aircraft information from list
        for count, item in enumerate(round_aircraft):
            file = round_aircraft[count][3] 
            filepath = f"{main_path}{file}.jpg"
            file_paths.append(filepath)
            aircraft_names.append(round_aircraft[count][0])

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

        # Display Rounds in Widget
        rounds_label = Label(root, text=f"Round {rounds_played + 1} of {how_many}", font=small_fontb)
        rounds_label.grid(row=0)

        # Display correct GUI depending on what mode user chooses
        button_frame = Frame(root)
        button_frame.grid(row=3)

        if imgname == "Image": # If user plays Guess the Image
            # Answer to choose label
            name_label = Label(root, text=f"Select the Image Below that is a\n{ans_name}", font=med_fontb, width=35)
            name_label.grid(row=1)

            # 4 Image display
            i1 = Image.open(file_paths[0]).resize((200, 144))
            img1 = ImageTk.PhotoImage(i1)
            i2 = Image.open(file_paths[1]).resize((200, 144))
            img2 = ImageTk.PhotoImage(i2)
            i3 = Image.open(file_paths[2]).resize((200, 144))
            img3 = ImageTk.PhotoImage(i3)
            i4 = Image.open(file_paths[3]).resize((200, 144))
            img4 = ImageTk.PhotoImage(i4)

            button1 = Button(button_frame, text="Button 1", font=med_font, image=img1, command=partial(self.round_results, 0),
                            border=1, relief="solid")
            button1.grid(row=0, column=0, padx=5)
            button1.image = img1

            button2 = Button(button_frame, image=img2, command=partial(self.round_results, 1),
                            border=1, relief="solid")
            button2.grid(row=0, column=1, padx=5)
            button2.image = img2

            button3 = Button(button_frame, image=img3, command=partial(self.round_results, 2),
                            border=1, relief="solid")
            button3.grid(row=1, column=0, padx=5)
            button3.image = img3

            button4 = Button(button_frame, image=img4, command=partial(self.round_results, 3),
                            border=1, relief="solid")
            button4.grid(row=1, column=1, padx=5)
            button4.image = img4

        else: # If users plays guess the name
            # Display Image for correct answer
            answer_image = ImageTk.PhotoImage(Image.open(ans_img).resize((250, 180)))
            image_label = Label(root, image=answer_image, border=1, relief="solid")
            image_label.grid(row=1, pady=5)
            image_label.image = answer_image
            # Small instructions label
            instructions_label = Label(root, text="Select the Name Below that\nCorresponds to the Image Above", font=small_fontb, width=30, height=2,
                            border=1, relief="solid")
            instructions_label.grid(row=2, pady=5)

            # 4 Name Display
            name1 = aircraft_names[0]
            name2 = aircraft_names[1]
            name3 = aircraft_names[2]
            name4 = aircraft_names[3]

            button1 = Button(button_frame, text=name1, width=20, height=2, wraplength=150,
                            border=1, relief="solid", command=partial(self.round_results, 0))
            button1.grid(row=0, column=0, padx=5)

            button2 = Button(button_frame, text=name2, width=20, height=2, wraplength=150,
                            border=1, relief="solid", command=partial(self.round_results, 1))
            button2.grid(row=0, column=1, padx=5)

            button3 = Button(button_frame, text=name3, width=20, height=2, wraplength=150,
                            border=1, relief="solid", command=partial(self.round_results, 2))
            button3.grid(row=1, column=0, padx=5)

            button4 = Button(button_frame, text=name4, width=20, height=2, wraplength=150, 
                            border=1, relief="solid", command=partial(self.round_results, 3))
            button4.grid(row=1, column=1, padx=5)

        answer_label = Label(root, text="Select the answer you think is\ncorrect and find out if you are.", font=small_font,
                            border=1, relief="solid")
        answer_label.grid(row=4, pady=5)

        next_button = Button(root, text="Next Round", font=med_fontb, command=self.next_round,
                            border=1, relief="solid")
        next_button.grid(row=5)

    def next_round(self):
        print()
        print("TESTING FUNCTION")
        print()

    def round_results(self, button_pressed):
        """
            Retrieves which button was pushed (index 0 - 3), retrives
            score and then compares it with median, updates results
            and adds results to stats list.
        """
        print("The Button Pressed Was: ", button_pressed)


# Main Routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
