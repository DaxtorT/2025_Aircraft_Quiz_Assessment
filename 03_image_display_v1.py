from tkinter import *
from PIL import ImageTk, Image

root = Tk()

i1 = Image.open("C:/Users/scrap/OneDrive - Massey High School/Year 13 (2025)/TCCOUE/Aircraft Quiz/Aircraft Data/Sikorsky-UH-60 Black-Hawk.jpg")
i2 = Image.open("C:/Users/scrap/OneDrive - Massey High School/Year 13 (2025)/TCCOUE/Aircraft Quiz/Aircraft Data/Boeing-747-8.jpg")
i3 = Image.open("C:/Users/scrap/OneDrive - Massey High School/Year 13 (2025)/TCCOUE/Aircraft Quiz/Aircraft Data/Sukhoi Su-25.jpg")
i4 = Image.open("C:/Users/scrap/OneDrive - Massey High School/Year 13 (2025)/TCCOUE/Aircraft Quiz/Aircraft Data/F7U Cutlass.jpg")
i1 = i1.resize((100, 72))
i2 = i2.resize((200, 144))
i3 = i3.resize((100, 72))
i4 = i4.resize((200, 144))
img1 = ImageTk.PhotoImage(i1)
img2 = ImageTk.PhotoImage(i2)
img3 = ImageTk.PhotoImage(i3)
img4 = ImageTk.PhotoImage(i4)

l1 = Label(root, image=img1)
l1.grid(row=0)

l2 = Label(root, image=img2)
l2.grid(row=1)

l3 = Label(root, image=img3)
l3.grid(row=2)

l4 = Label(root, image=img4)
l4.grid(row=3)

mainloop()
