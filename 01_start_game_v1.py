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

        bg_path = "C:/Users/scrap/OneDrive - Massey High School/Year 13 (2025)/TCCOUE/Aircraft Quiz/Documentation/aircraft_background.jpg"  # Use correct relative path
        bg_img = Image.open(bg_path)
        resize_img = bg_img.resize((500, 720), Image.Resampling.LANCZOS)  # Resize to fit window
        self.bg_img = ImageTk.PhotoImage(resize_img)


        self.start_bg = Label(root, image=self.bg_img)
        self.start_bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.start_bg.image = self.bg_img

        self.start_frame = Frame(root)
        self.start_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.start_heading = Label(self.start_frame,
                                   text="Welcome To\nThe Best Aircraft Quiz",
                                   font=("B612", "16", "bold"), width=25, border=1, relief="solid")
        self.start_heading.grid(row=1)
        

# Main Routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    root.geometry("500x720")
    root.resizable(False, False)
    #root.grid_rowconfigure(0, weight=1)
    #root.grid_columnconfigure(0, weight=1)
    StartGame()
    root.mainloop()