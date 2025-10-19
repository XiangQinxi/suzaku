from suzaku import *

root = Sk()
root.bind("delay[5]", lambda _: print("Delay 5"))

root.mainloop()
