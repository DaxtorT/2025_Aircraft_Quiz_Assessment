from tkinter import *
from PIL import ImageTk, Image

class Images():
    """
    Main Image Testing Class
    """
    def __init__(self):
        """
        Image Buttons GUI Test
        """
        # Set the images to usable variables
        i1 = Image.open("C:/Users/scrap/OneDrive - Massey High School/Year 13 (2025)/TCCOUE/Aircraft Quiz/Aircraft Data/Sikorsky-UH-60 Black-Hawk.jpg")
        i2 = Image.open("C:/Users/scrap/OneDrive - Massey High School/Year 13 (2025)/TCCOUE/Aircraft Quiz/Aircraft Data/Boeing-747-8.jpg")
        i3 = Image.open("C:/Users/scrap/OneDrive - Massey High School/Year 13 (2025)/TCCOUE/Aircraft Quiz/Aircraft Data/Sukhoi Su-25.jpg")
        i4 = Image.open("C:/Users/scrap/OneDrive - Massey High School/Year 13 (2025)/TCCOUE/Aircraft Quiz/Aircraft Data/F7U Cutlass.jpg")
        i1 = i1.resize((100, 72))
        i2 = i2.resize((200, 144))
        i3 = i3.resize((100, 72))
        i4 = i4.resize((200, 144))
        i1 = ImageTk.PhotoImage(i1)
        i2 = ImageTk.PhotoImage(i2)
        i3 = ImageTk.PhotoImage(i3)
        i4 = ImageTk.PhotoImage(i4)

        # Display the images on widgets
        l1 = Label(root, image=i1, border=1, relief="solid")
        l1.grid(row=0)

        l2 = Label(root, image=i2, border=1, relief="solid")
        l2.grid(row=1)

        l3 = Label(root, image=i3, border=1, relief="solid")
        l3.grid(row=2)
        l3.image = i3

        l4 = Label(root, image=i4, border=1, relief="solid")
        l4.grid(row=3)
        l4.image = i4

if __name__ == "__main__":
    root = Tk()
    root.title("The Best Aircraft Quiz")
    Images()
    root.mainloop()