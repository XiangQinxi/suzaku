from tkinter import *


root = Tk()

photo = PhotoImage(file="custom_rounded_rect.png")

img = Label(image=photo)
img.pack()

root.mainloop()
