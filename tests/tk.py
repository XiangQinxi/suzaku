from tkinter import ttk
from tkinter import *

root = Tk()
labeled_scale = ttk.LabeledScale(root, from_=0, to=100)
labeled_scale.pack()
root.mainloop()
