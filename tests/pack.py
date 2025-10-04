from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk


root = ThemedTk(theme="ubuntu")
root.geometry("300x300")

frame1 = ttk.Frame(root)

button = ttk.Button(frame1, text="Button 1")
button.pack()

button2 = ttk.Button(frame1, text="Button 1")
button2.pack()

button3 = ttk.Button(frame1, text="Button 1")
button3.pack(anchor="nw")

button3 = ttk.Button(frame1, text="Button 1")
button3.pack(anchor="ne")

# frame1.pack(fill="both", ipadx=5, ipady=5, padx=5, pady=5)

frame2 = ttk.Frame(root)

ttk.Button(frame2, text="Button 1").pack()

ttk.Button(frame2, text="Button 2").pack(side="left")

ttk.Button(frame2, text="Button 3").pack(side="left")

ttk.Button(frame2, text="Button 4").pack(side="left")

ttk.Button(frame2, text="Button 5").pack(side="right")

ttk.Button(frame2, text="Button 6").pack()

ttk.Button(frame2, text="Button 7").pack(side="left")

ttk.Button(frame2, text="Button 8").pack(side="left")

ttk.Button(frame2, text="Button 9").pack(side="right")

# frame2.pack(fill="both", ipadx=5, ipady=5, padx=5, pady=5)

"""ttk.Button(root, text="Button 1").pack(side="left")

ttk.Button(root, text="Button 2").pack(side="left")

ttk.Button(root, text="Button 3").pack(side="right")

ttk.Button(root, text="Button 4").pack(side="right")

ttk.Button(root, text="Button 5").pack(side="top", fill="y", expand=True)

ttk.Button(root, text="Button 6").pack(side="bottom")"""

ttk.Button(root, text="Button 1").pack(side="top")

ttk.Button(root, text="Button 2").pack(side="top")

ttk.Button(root, text="Button 3").pack(side="bottom")

ttk.Button(root, text="Button 4").pack(side="bottom")

ttk.Button(root, text="Button 5").pack(side="left", fill="x", expand=True)

ttk.Button(root, text="Button 6").pack(side="right")

root.mainloop()
