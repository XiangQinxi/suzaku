from suzaku import *


root = Sk()

image = SkImage(root, "checkmark.png")
image.resize(50, 50)
image.box()

root.mainloop()
