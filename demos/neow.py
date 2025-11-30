from suzaku import *


root = Sk()

button = SkTextButton(root, text="Click me")
button.grid(column=0, row=0)
button2 = SkTextButton(root, text="Click me")
button2.grid(column=0, row=1)

root.mainloop()
