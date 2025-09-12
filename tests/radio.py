from suzaku import *


root = Sk()

radiobox = SkRadioBox(root)
radiobox.box()

radioitem = SkRadioItem(root, text="123")
radioitem.box()

root.mainloop()
