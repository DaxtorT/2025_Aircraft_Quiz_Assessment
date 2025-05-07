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
        # Radiobutton color when selected
        col = "#dddddd"

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
        # Guess Image or Name Buttons
        self.imgname_filt.set(0)
        self.guess_img_but = Radiobutton(self.in_filt_frame, variable=self.imgname_filt, value=0,
                                    text="Guess The Image", indicatoron=0, selectcolor=col,
                                    font=("B612", "10"), width=13, height=2, border=1, relief="solid")
        self.guess_img_but.grid(row=0, column=0)
        self.guess_name_but = Radiobutton(self.in_filt_frame, variable=self.imgname_filt, value=1,
                                    text="Guess The Name", indicatoron=0, selectcolor=col,
                                    font=("B612", "10"), width=13, height=2, border=1, relief="solid")
        self.guess_name_but.grid(row=0, column=1)

        # Plane, Heli Filter Frame
        self.ph_filt_frame = Frame(root)
        self.ph_filt_frame.place(x=140, y=285)
        # Plane, Both, Heli Filter Buttons
        self.planeheli_filt.set(0)
        self.plane_filt_but = Radiobutton(self.ph_filt_frame, variable=self.planeheli_filt, value=1,
                                    text="Plane", indicatoron=0, selectcolor=col,
                                    font=("B612", "10"), width=9, height=2, border=1, relief="solid")
        self.plane_filt_but.grid(row=0, column=0)
        self.both_filt_but = Radiobutton(self.ph_filt_frame, variable=self.planeheli_filt, value=0,
                                    text="Both", indicatoron=0, selectcolor=col,
                                    font=("B612", "10"), width=7, height=2, border=1, relief="solid")
        self.both_filt_but.grid(row=0, column=1)
        self.heli_filt_but = Radiobutton(self.ph_filt_frame, variable=self.planeheli_filt, value=2,
                                    text="Helicopters", indicatoron=0, selectcolor=col,
                                    font=("B612", "10"), width=9, height=2, border=1, relief="solid")
        self.heli_filt_but.grid(row=0, column=2)

        # Civ, Mil Filter Frame
        self.cm_filt_frame = Frame(root)
        self.cm_filt_frame.place(x=140, y=355)
        # Civilain, Both, Military Filter Buttons
        self.civmil_filt.set(0)
        self.civ_filt_but = Radiobutton(self.cm_filt_frame, variable=self.civmil_filt, value=1,
                                    text="Civilian", indicatoron=0, selectcolor=col,
                                    font=("B612", "10"), width=9, height=2, border=1, relief="solid")
        self.civ_filt_but.grid(row=0, column=0)
        self.cm_filt_but = Radiobutton(self.cm_filt_frame, variable=self.civmil_filt, value=0,
                                    text="Both", indicatoron=0, selectcolor=col,
                                    font=("B612", "10"), width=7, height=2, border=1, relief="solid")
        self.cm_filt_but.grid(row=0, column=1)
        self.mil_filt_but = Radiobutton(self.cm_filt_frame, variable=self.civmil_filt, value=2,
                                    text="Military", indicatoron=0, selectcolor=col,
                                    font=("B612", "10"), width=9, height=2, border=1, relief="solid")
        self.mil_filt_but.grid(row=0, column=2)

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