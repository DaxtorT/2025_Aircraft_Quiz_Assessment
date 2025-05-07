from tkinter import *
from PIL import ImageTk, Image

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
        self.start_instruct = Label(root, text="*Placeholder Instructions*",
                                   font=("B612", "12", "bold"), width=40, height=3, border=1, relief="solid")
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
            [self.in_filt_frame, "Guess The Image", self.imgname_filt, 0, 13, 0],
            [self.in_filt_frame, "Guess The Name", self.imgname_filt, 1, 13, 1],
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
                                          font=("B612", "10"), selectcolor="#dddddd", height=2, border=1, relief="solid", indicatoron=0)
            self.make_radio.grid(row=0, column=item[5])
            self.radios_ref_list.append(self.make_radio)

        # Ask user quiz rounds
        self.round_instruct = Label(root, text="*Placeholder Instructions*",
                                   font=("B612", "12", "bold"), width=22, height=2, border=1, relief="solid")
        self.round_instruct.place(x=140, y=500)

        self.round_entry = Entry(root, font=("B612", "16"), width=17, border=1, relief="solid", justify="center")
        self.round_entry.place(x=139, y=550)

        # End & Start Game Buttons
        self.end_game_but = Button(root, text="🚫 End Quiz 🚫", command=self.end_quiz,
                                   font=("B612", "16", "bold"), width=13, border=1, relief="solid")
        self.end_game_but.place(x=30, y=650)

        self.start_game_but = Button(root, text="✅ Play Quiz ✅", command=self.start_quiz,
                                     font=("B612", "16", "bold"), width=13, border=1, relief="solid")
        self.start_game_but.place(x=295, y=650)

    def end_quiz(self):
        print("End Quiz")
    
    def start_quiz(self):
        print("Start Quiz")

# Main Routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    root.geometry("500x720")
    root.resizable(False, False)
    StartGame()
    root.mainloop()