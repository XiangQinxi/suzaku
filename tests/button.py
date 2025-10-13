from suzaku import *


root = Sk()

button = SkButton(root, command=lambda: print("Click"))

button.box()

root.mainloop()
